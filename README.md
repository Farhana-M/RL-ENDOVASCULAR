# Benchmarking Reinforcement Learning Algorithms for Autonomous Mechanical Thrombectomy

This repository provides a benchmark of four model-free reinforcement learning algorithms (**DDPG**, **TD3**, **SAC**, and **PPO**) for autonomous navigation in endovascular environments.  
The benchmark tasks **use the** **ArchVariety** and **DualDeviceNav** environments from the `stEVE_bench` suite.

All algorithms are implemented using the `stable-baselines3` library, and training is performed under both default and tuned hyperparameter configurations.

Full experimental details and results are available in the accompanying paper:

**"Benchmarking Reinforcement Learning Algorithms for Autonomous Mechanical Thrombectomy"**

---

## 🔗 Dependencies

- [`stEVE`](https://github.com/lkarstensen/stEVE): Simulation framework for endovascular interventions based on SOFA and compatible with Gymnasium.
- [`stEVE_bench`](https://github.com/lkarstensen/stEVE_bench): Collection of benchmark environments built on stEVE for evaluating robotic endovascular navigation.
- [`stable-baselines3`](https://github.com/DLR-RM/stable-baselines3): A set of reliable implementations of reinforcement learning algorithms in PyTorch.

---

## 🛠️ Installation

```bash
# (optional) Activate your Python virtual environment

# Ensure stEVE and stEVE_bench are cloned and installed
# Refer to their respective README files for setup instructions

# Clone and install this benchmark repository
git clone https://github.com/Farhana-M/RL-ENDOVASCULAR
cd RL-ENDOVASCULAR
pip install -r requirements.txt
```

📌 **Important:** Replace the file `eve_bench/archvariety.py` in `stEVE_bench` with the modified `archvariety.py` located in the `envs/` folder of this repository to ensure benchmark compatibility.

---
## 📁 Recommended Project Layout

```bash
<your_workspace>/
│
├── stEVE/                       # Cloned from https://github.com/lkarstensen/stEVE
│
├── stEVE_bench/                 # Cloned from https://github.com/lkarstensen/stEVE_bench
│
├── RL-ENDOVASCULAR/             # This repository
│   ├── benchmark_archvariety.py
│   ├── configs/
│   │   ├── experiment1.yaml     # Default hyperparameter settings
│   │   └── experiment2.yaml     # Hyperparameter tuning variants
│   ├── models/                  # Checkpoints saved here after training (auto-generated)
│   ├── logs/                    # Evaluation logs saved here (auto-generated)
│   ├── envs/
│   │   └── archvariety.py       # Replace in stEVE_bench
│   ├── requirements.txt
│   └── README.md

---

## Running Experiments

### Experiment 1 – Default Hyperparameters
Run an RL algorithm using default parameters:

```bash
python benchmark_archvariety.py --config configs/experiment1.yaml --algo td3
```

Change the `--algo` argument to one of the supported algorithms: `ddpg`, `td3`, `sac`, or `ppo`.

### Experiment 2 – Hyperparameter Tuning
Run a tuning variant (e.g., alternative network architecture or learning rate):

```bash
python benchmark_archvariety.py \
    --config configs/experiment2.yaml \
    --base_config configs/experiment1.yaml \
    --algo sac \
    --tuning_config lr_1e-3
```

📌 For Experiment 2, specify both `--algo` and the corresponding `--tuning_config`.

---

## Benchmark Results (as reported in our paper)

| Environment         | Algorithm | Success Rate (%) | Procedure Time (s) | Path Ratio (%) | Exploration Steps |
|---------------------|-----------|------------------|---------------------|----------------|-------------------|
| ArchVariety (default) | DDPG     | 80               | 6.87                | 78.8           | 6.75 × 10⁶        |
|                     | TD3       | 79               | 14.04               | 61.1           | 8.25 × 10⁶        |
|                     | SAC       | 66               | 7.49                | 71.0           | 7.25 × 10⁶        |
|                     | PPO       | 70               | 5.5                 | 67.7           | 7.5 × 10⁶         |
| ArchVariety (tuned) | SAC       | 70               | 7.72                | 71.6           | 6.75 × 10⁶        |
|                     | PPO       | 84               | 5.08                | 77.3           | 9.75 × 10⁶        |
| DualDeviceNav (tuned) | DDPG     | 24               | 88.62               | 55             | 1.0 × 10⁶         |
|                     | TD3       | 68               | 214.05              | 62             | 2.5 × 10⁶         |
|                     | SAC       | 58               | 182.98              | 66             | 8.25 × 10⁶        |
|                     | PPO       | 41               | 574.33              | 66             | 6.5 × 10⁶         |

---

## 📬 Citation

If you use this benchmark, please cite:

---

## 📝 License

MIT License (see `LICENSE` file).