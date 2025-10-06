# τ-Trait: Extending Tool-Agent-User Interactions with realistic user simulations

## Collinear AI 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Tau-Trait** is a benchmark for evaluating large language models (LLMs) with **realistic, persona-aware simulations**. It builds on Tau-Bench but introduces two key modifications:

1. **TraitBasis-generated personas** – more accurate and interpretable user simulations.
2. **Domain-specific evaluation** – tasks drawn from **retail, airline, telecom, and telehealth** settings.

Tau-Trait is designed to test model **robustness, personalization, and fairness** in high-impact, customer-facing domains where user traits strongly influence interaction quality.

## Results  

| Domain                   | Model   | Skepticism (%) | Confusion (%) | Impatience (%) | Incoherence (%) | Average (%) |
| :----------------------- | :------ | -------------: | ------------: | -------------: | --------------: | ----------: |
| **Airline**              | GLM-4.5 |          -11.0 |         -16.9 |          -12.8 |           -12.2 |       -13.2 |
|                          | GPT-4o  |           -6.7 |          -5.0 |           -4.4 |            -6.7 |        -5.7 |
|                          | Kimi K2 |          -11.8 |          -9.5 |           -6.2 |            -7.1 |        -8.7 |
| **Retail**               | GLM-4.5 |            0.2 |          -5.4 |           -2.6 |            -0.5 |        -2.1 |
|                          | GPT-4o  |          -29.2 |         -34.2 |          -25.9 |           -22.9 |       -28.1 |
|                          | Kimi K2 |          -21.9 |         -45.7 |          -31.2 |           -21.4 |       -30.0 |
| **Telecom & Telehealth** | GLM-4.5 |            0.8 |         -16.8 |           -3.9 |            -2.3 |        -5.5 |
|                          | GPT-4o  |          -11.5 |         -14.0 |          -16.9 |            -8.7 |       -12.8 |
|                          | Kimi K2 |          -11.4 |         -18.1 |          -14.7 |            -4.5 |       -12.2 |

## τ-Trait vs τ-Bench rollouts 

![Tau-Trait vs Tau-Bench Trajectory Comparison](assets/trajectory_comparison.png)

---

## ✨ Features

* **Persona Simulation with TraitBasis**
  Generate diverse, coherent user personas with different traits.

* **Domain Coverage**
  Tau-Trait includes evaluation tasks in **four industries**:

  * 🛒 **Retail** 
  * ✈️ **Airline** 
  * 📱 **Telecom** 
  * 🩺 **Telehealth** 

## 🚀 Getting Started

### Installation

```bash
conda create -n tau_trait -y python=3.11
conda activate tau_trait
pip install jupyterlab ipykernel nest_asyncio jinja2 --no-cache
pip install "openai>=1.13.3" "mistralai>=0.4.0" "anthropic>=0.26.1" "google-generativeai>=0.5.4" "tenacity>=8.3.0" "termcolor>=2.4.0" "numpy>=1.26.4" "litellm==1.41.0"
pip install -e .
```

## Usage

### Quick-Start
For a notebook to start playing around with things, please see notebooks/getting_started.ipynb

### Run Config Info

```
import argparse
from tau_trait.types import RunConfig
from tau_trait.run import run
from litellm import provider_list
from tau_trait.envs.user import UserStrategy

from tau_trait.types import RunConfig
from tau_trait.run import run

config = RunConfig(
    model_provider="openai",
    user_model_provider="steer",
    model=CLIENT_ASSISTANT_MODEL_NAME,
    user_model="", # steer api abstracts the model
    num_trials=1,
    env="retail",
    agent_strategy="tool-calling",
    temperature=0.7,
    task_split="test",
    start_index=0,
    end_index=-1,
    task_ids=[4],
    log_dir="results",
    max_concurrency=1,
    seed=10,
    shuffle=0,
    user_strategy="trait-mix",
    few_shot_displays_path=None,
    trait_dict={"impatience": 1, "confusion": 0, "skeptical": 0, "incoherence": 0},
)
```

Some definitions of the settings are below.

### Tau-Trait Config Settings
**General**
- **`--num-trials`** *(int, default: 1)*  
  Number of independent trials to run.

- **`--seed`** *(int, default: 10)*  
  Random seed for reproducibility.

- **`--shuffle`** *(int, default: 0)*  
  Whether to shuffle task order (0 = no, 1 = yes).

- **`--log-dir`** *(str, default: `results`)*  
  Directory where logs and results are stored.

**Environment & Tasks**
- **`--env`** *(str, choices: `retail`, `airline`, default: `retail`)*  
  Domain environment in which to run simulations.

- **`--task-split`** *(str, choices: `train`, `test`, `dev`, default: `test`)*  
  Dataset split of tasks to run (applies only to the retail domain currently).

- **`--start-index`** *(int, default: 0)*  
  Index of the first task to run.

- **`--end-index`** *(int, default: -1)*  
  Index of the last task to run. Use `-1` to run all remaining tasks.

- **`--task-ids`** *(list of int, optional)*  
  Explicit list of task IDs to run (overrides index ranges).

**Agent Configuration**
- **`--model`** *(str, required)*  
  The model to use for the **agent**.

- **`--model-provider`** *(str, choices from `provider_list`)*  
  Provider for the agent’s model.

- **`--temperature`** *(float, default: 0.0)*  
  Sampling temperature for the action model (higher = more randomness).

- **`--few-shot-displays-path`** *(str, optional)*  
  Path to a JSONL file containing few-shot demonstration examples.

**User Simulator Configuration**
- **`--user-model`** *(str, default: `gpt-4o`)*  
  Model to use for the **user simulator**.

- **`--user-model-provider`** *(str, optional)*  
  Provider for the user simulator’s model.

- **`--user-strategy`** *(str, choices from `UserStrategy`, default: `llm`)*  
  Strategy for the simulated user (e.g., LLM-based).

### Execution Controls
- **`--max-concurrency`** *(int, default: 1)*  
  Number of tasks to run in parallel.

```
@misc{tau-trait,
  author       = {Mackey, Tsach; Rajeev, Meghana; Kumar, Anand; He, Muyu; Rajani, Nazneen},
  title        = {Tau-Trait},
  year         = {2025},
  month        = {Sep},
  howpublished = {\url{https://pypi.org/project/tau-trait/}}
}
```