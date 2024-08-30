import gymnasium as gym
import eve
import numpy as np
import csv
import os
import re

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, CallbackList
#from eve_bench import ArchVariety
from eve_bench9 import ArchVariety as ArchVariety9
from eve_bench10 import ArchVariety as ArchVariety10


from time import perf_counter

def make_env():
    intervention = ArchVariety9()
    start = eve.start.InsertionPoint(intervention=intervention)
    pathfinder = eve.pathfinder.BruteForceBFS(intervention=intervention)

    position = eve.observation.Tracking2D(intervention=intervention, n_points=3, resolution=2.0)
    position = eve.observation.wrapper.NormalizeTracking2DEpisode(position, intervention)
    position = eve.observation.wrapper.Memory(position, 2, eve.observation.wrapper.MemoryResetMode.FILL)

    target_state = eve.observation.Target2D(intervention=intervention)
    target_state = eve.observation.wrapper.NormalizeTracking2DEpisode(target_state, intervention)

    last_action = eve.observation.LastAction(intervention)
    last_action = eve.observation.wrapper.Normalize(last_action)

    state = eve.observation.ObsDict({
        "position": position, 
        "target": target_state, 
        "last_action": last_action
    })

    target_reward = eve.reward.TargetReached(intervention=intervention, factor=1.0)
    step_reward = eve.reward.Step(factor=-0.005)
    path_delta = eve.reward.PathLengthDelta(pathfinder=pathfinder, factor=0.001)
    reward = eve.reward.Combination([target_reward, path_delta, step_reward])

    target_reached = eve.terminal.TargetReached(intervention=intervention)
    max_steps = eve.truncation.MaxSteps(200)
    vessel_end = eve.truncation.VesselEnd(intervention)
    truncation = eve.truncation.Combination([max_steps, vessel_end])

    path_ratio = eve.info.PathRatio(pathfinder)
    steps = eve.info.Steps()
    trans_speed = eve.info.AverageTranslationSpeed(intervention)
    trajectory_length = eve.info.TrajectoryLength(intervention)
    info = eve.info.Combination([path_ratio, steps, trans_speed, trajectory_length])

    return eve.Env(
        intervention=intervention,
        observation=state,
        reward=reward,
        terminal=target_reached,
        truncation=truncation,
        start=start,
        pathfinder=pathfinder,
        info=info,
        interim_target=None,
    )

def make_eval_env():
    intervention = ArchVariety10()
    start = eve.start.InsertionPoint(intervention=intervention)
    pathfinder = eve.pathfinder.BruteForceBFS(intervention=intervention)

    position = eve.observation.Tracking2D(intervention=intervention, n_points=3, resolution=2.0)
    position = eve.observation.wrapper.NormalizeTracking2DEpisode(position, intervention)
    position = eve.observation.wrapper.Memory(position, 2, eve.observation.wrapper.MemoryResetMode.FILL)

    target_state = eve.observation.Target2D(intervention=intervention)
    target_state = eve.observation.wrapper.NormalizeTracking2DEpisode(target_state, intervention)

    last_action = eve.observation.LastAction(intervention)
    last_action = eve.observation.wrapper.Normalize(last_action)

    state = eve.observation.ObsDict({
        "position": position, 
        "target": target_state, 
        "last_action": last_action
    })

    target_reward = eve.reward.TargetReached(intervention=intervention, factor=1.0)
    step_reward = eve.reward.Step(factor=-0.005)
    path_delta = eve.reward.PathLengthDelta(pathfinder=pathfinder, factor=0.001)
    reward = eve.reward.Combination([target_reward, path_delta, step_reward])

    target_reached = eve.terminal.TargetReached(intervention=intervention)
    max_steps = eve.truncation.MaxSteps(200)
    vessel_end = eve.truncation.VesselEnd(intervention)
    truncation = eve.truncation.Combination([max_steps, vessel_end])

    path_ratio = eve.info.PathRatio(pathfinder)
    steps = eve.info.Steps()
    trans_speed = eve.info.AverageTranslationSpeed(intervention)
    trajectory_length = eve.info.TrajectoryLength(intervention)
    info = eve.info.Combination([path_ratio, steps, trans_speed, trajectory_length])

    return eve.Env(
        intervention=intervention,
        observation=state,
        reward=reward,
        terminal=target_reached,
        truncation=truncation,
        start=start,
        pathfinder=pathfinder,
        info=info,
        interim_target=None,
    )
class CustomEvalCallback(BaseCallback):
    def __init__(self, eval_env, eval_freq, log_path, verbose=1):
        super().__init__(verbose)
        self.eval_env = eval_env
        self.eval_freq = eval_freq
        self.log_path = log_path
        self.next_eval_step = eval_freq
        self.num_episodes = 100

    def _on_step(self):
        if self.num_timesteps >= self.next_eval_step:
            self.success_count = 0
            self.total_navigation_time = 0
            self.path_ratio_unsuccessful = []

            for _ in range(self.num_episodes):
                obs, info = self.eval_env.reset()
                done = False
                start_time = perf_counter()
                while not done:
                    action, _states = self.model.predict(obs, deterministic=True)
                    obs, reward, terminal, truncation, info = self.eval_env.step(action)
                    done = terminal or truncation
                    if terminal:
                        self.success_count += 1
                        self.total_navigation_time += perf_counter() - start_time
                    elif truncation:
                        self.path_ratio_unsuccessful.append(info.get('path_ratio', 0))

            self.log_results()
            self.next_eval_step += self.eval_freq

        return True

    def log_results(self):
        success_rate = self.success_count / self.num_episodes
        mean_navigation_time = self.total_navigation_time / self.success_count if self.success_count > 0 else 0
        mean_path_ratio = np.mean(self.path_ratio_unsuccessful) if self.path_ratio_unsuccessful else 0

        with open(self.log_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.num_timesteps, f"{success_rate:.2f}", f"{mean_navigation_time:.2f}", f"{mean_path_ratio:.8f}"])

        if self.verbose > 0:
            print(f"Evaluated at {self.num_timesteps} steps:")
            print(f" Success Rate: {success_rate * 100:.2f}%")
            print(f" Mean Navigation Time: {mean_navigation_time:.2f} seconds")

def find_latest_checkpoint(directory, prefix):
    max_timestep = -1
    latest_model_path = None
    pattern = re.compile(rf"{prefix}_([0-9]+)\.zip")
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            timestep = int(match.group(1))
            if timestep > max_timestep:
                max_timestep = timestep
                latest_model_path = os.path.join(directory, filename)
    return latest_model_path

if __name__ == "__main__":
    num_envs = 25
    train_env = SubprocVecEnv([make_env for _ in range(num_envs)])
    eval_env = make_env()

    model_path = "/nfs/home/agranados/projects/RL/Scripts/batch_sixteen"
    model_prefix = "ppo_model_16_lr_checkpoint"
    latest_model = find_latest_checkpoint(model_path, model_prefix)


    if latest_model:
        model = PPO.load(latest_model, env=train_env)
        current_timestep = int(re.search(r"(\d+)\.zip", latest_model).group(1))
        print(f"Resuming training from checkpoint: {latest_model} at timestep {current_timestep}")
    else:
        model = PPO("MultiInputPolicy", train_env, verbose=1, seed =42)
        current_timestep = 0
        print("Starting training from scratch")

    eval_callback = CustomEvalCallback(eval_env, eval_freq=250000, log_path="/nfs/home/agranados/projects/RL/Scripts/batch_sixteen/ppo_model_16_lr_results.csv", verbose=1)

    total_timesteps = 1e7
    save_interval = 250000

    while current_timestep < total_timesteps:
        steps_to_run = min(save_interval, total_timesteps - current_timestep)
        model.learn(total_timesteps=steps_to_run, reset_num_timesteps=False, callback=eval_callback)

        current_timestep += steps_to_run
        interim_save_path = f"{model_path}/ppo_model_16_lr_checkpoint_{current_timestep}.zip"
        model.save(interim_save_path)
        print(f"Checkpoint saved at {interim_save_path}")

    final_model_path = f"{model_path}/ppo_model_16_lr_final.zip"
    model.save(final_model_path)
    print(f"Final model saved at: {final_model_path}")

    train_env.close()
    eval_env.close()
