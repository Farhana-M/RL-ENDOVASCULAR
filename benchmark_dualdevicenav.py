import argparse
import os
import re
import yaml
import csv
import numpy as np
import gymnasium as gym
import sys
import eve
import eve.visualisation
from time import perf_counter
from typing import Optional
from stable_baselines3 import PPO, SAC, TD3, DDPG
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.noise import NormalActionNoise
from eve_bench.dualdevicenav import DualDeviceNav

def get_model_class(algo_name):
    algo_name = algo_name.lower()
    if algo_name == "ddpg":
        return DDPG
    elif algo_name == "td3":
        return TD3
    elif algo_name == "sac":
        return SAC
    elif algo_name == "ppo":
        return PPO
    else:
        raise ValueError(f"Unsupported algorithm: {algo_name}")

def create_train_env(cfg):
    return _create_env(cfg)

def create_eval_env(cfg):
    return _create_env(cfg)

def _create_env(cfg):
    intervention = DualDeviceNav(
        normalize_action=cfg.get("normalize_action", False)
    )
    start = eve.start.InsertionPoint(intervention=intervention)
    pathfinder = eve.pathfinder.BruteForceBFS(intervention=intervention)

    position_device1 = eve.observation.Tracking2D(intervention=intervention, n_points=3, resolution=2.0, name="guid")
    position_device1 = eve.observation.wrapper.NormalizeTracking2DEpisode(position_device1, intervention)
    position_device1 = eve.observation.wrapper.Memory(position_device1, 2, eve.observation.wrapper.MemoryResetMode.FILL)

    position_device2 = eve.observation.TrackingDevice2D(intervention=intervention, device_idx=1, n_points=3, resolution=2.0, name="cath")
    position_device2 = eve.observation.wrapper.NormalizeTracking2DEpisode(position_device2, intervention)
    position_device2 = eve.observation.wrapper.Memory(position_device2, 2, eve.observation.wrapper.MemoryResetMode.FILL)

    target_state = eve.observation.Target2D(intervention=intervention)
    target_state = eve.observation.wrapper.NormalizeTracking2DEpisode(target_state, intervention)

    last_action = eve.observation.LastAction(intervention)
    last_action = eve.observation.wrapper.Normalize(last_action)

    state = eve.observation.ObsDict({
        "position_device1": position_device1,
        "position_device2": position_device2,
        "target": target_state,
        "last_action": last_action,
    })

    reward = eve.reward.Combination([
        eve.reward.TargetReached(intervention=intervention, factor=1.0),
        eve.reward.PathLengthDelta(pathfinder=pathfinder, factor=0.001),
        eve.reward.Step(factor=-0.005),
    ])

    terminal = eve.terminal.TargetReached(intervention=intervention)
    truncation = eve.truncation.Combination([
        eve.truncation.MaxSteps(500),
        eve.truncation.VesselEnd(intervention=intervention),
    ])

    info = eve.info.Combination([
        eve.info.PathRatio(pathfinder),
        eve.info.Steps(),
        eve.info.AverageTranslationSpeed(intervention),
        eve.info.TrajectoryLength(intervention),
    ])

    return eve.Env(
        intervention=intervention,
        observation=state,
        reward=reward,
        terminal=terminal,
        truncation=truncation,
        start=start,
        pathfinder=pathfinder,
        info=info,
        interim_target=None,
    )

class CustomEvalCallback(BaseCallback):
    def __init__(self, eval_env, eval_freq, log_path, start_step=0, verbose=1):
        super().__init__(verbose)
        self.eval_env = eval_env
        self.eval_freq = eval_freq
        self.log_path = log_path
        self.next_eval_step = start_step + eval_freq
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
                    action, _ = self.model.predict(obs, deterministic=True)
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
        procedure_time = self.total_navigation_time / self.success_count if self.success_count > 0 else 0
        path_ratio = np.mean(self.path_ratio_unsuccessful) if self.path_ratio_unsuccessful else 0

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        write_header = not os.path.exists(self.log_path) or os.stat(self.log_path).st_size == 0

        with open(self.log_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["Timesteps", "Success Rate", "Procedure Time (s)", "Path Ratio"])
            writer.writerow([self.num_timesteps, f"{success_rate:.2f}", f"{procedure_time:.2f}", f"{path_ratio:.8f}"])

        if self.verbose > 0:
            print(f"Evaluated at {self.num_timesteps} steps: Success Rate={success_rate:.2%}, Procedure Time={procedure_time:.2f}s")

def find_latest_checkpoint(directory, prefix):
    max_timestep = 0
    latest_model_path = None
    pattern = re.compile(rf"{prefix}_(\d+)\.zip")
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            timestep = int(match.group(1))
            if timestep > max_timestep:
                max_timestep = timestep
                latest_model_path = os.path.join(directory, filename)
    return latest_model_path, max_timestep

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    parser.add_argument("--algo", type=str, required=True, help="Algorithm to use: ddpg, td3, sac, ppo")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    algo = args.algo.lower()
    ModelClass = get_model_class(algo)
    algo_cfg = cfg[algo]

    train_env_cfg = algo_cfg["train_env"]
    eval_env_cfg = algo_cfg["eval_env"]
    train_cfg = algo_cfg["train"]

    num_envs = train_cfg["num_envs"]
    train_env = SubprocVecEnv([lambda: create_train_env(train_env_cfg) for _ in range(num_envs)])
    eval_env = create_eval_env(eval_env_cfg)

    noise_std = train_cfg.get("action_noise", {}).get("stddev", 0.1)
    action_noise = None
    if algo in ["ddpg", "td3"]:
        action_noise = NormalActionNoise(mean=np.zeros((1, 2)), sigma=noise_std * np.ones((1, 2)))

    model_path = train_cfg["model_path"]
    model_prefix = train_cfg["checkpoint_prefix"]
    os.makedirs(model_path, exist_ok=True)

    latest_model, current_step = find_latest_checkpoint(model_path, model_prefix)

    if latest_model:
        model = ModelClass.load(latest_model, env=train_env)
        print(f"Resuming from checkpoint: {latest_model} at {current_step} steps")
    else:
        current_step = 0
        model_kwargs = dict(
            policy="MultiInputPolicy",
            env=train_env,
            verbose=1,
            seed=42,
        )
        if action_noise:
            model_kwargs["action_noise"] = action_noise
        if "policy_kwargs" in train_cfg:
            model_kwargs["policy_kwargs"] = train_cfg["policy_kwargs"]
        if "learning_rate" in train_cfg:
            model_kwargs["learning_rate"] = train_cfg["learning_rate"]

        model = ModelClass(**model_kwargs)

    callback = CustomEvalCallback(
        eval_env,
        eval_freq=train_cfg["eval_freq"],
        log_path=train_cfg["log_path"],
        start_step=current_step
    )

    total_timesteps = int(train_cfg["total_timesteps"])
    save_interval = int(train_cfg["save_interval"])

    while current_step < total_timesteps:
        steps_to_run = min(save_interval, total_timesteps - current_step)
        model.learn(total_timesteps=steps_to_run, reset_num_timesteps=False, callback=callback)
        current_step += steps_to_run

        interim_path = os.path.join(model_path, f"{model_prefix}_{current_step}.zip")
        model.save(interim_path)
        print(f"Checkpoint saved: {interim_path}")

    final_model_path = os.path.join(model_path, f"{model_prefix}_final.zip")
    model.save(final_model_path)
    print(f"Final model saved: {final_model_path}")

    train_env.close()
    eval_env.close()
