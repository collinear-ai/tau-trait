# Tau-Trait

## Collinear AI 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Tau-Trait** is a benchmark for evaluating large language models (LLMs) with **realistic, persona-aware simulations**. It builds on Tau-Bench but introduces two key modifications:

1. **TraitBasis-generated personas** – more accurate and interpretable user simulations.
2. **Domain-specific evaluation** – tasks drawn from **retail, airline, telecom, and telehealth** settings.

Tau-Trait is designed to test model **robustness, personalization, and fairness** in high-impact, customer-facing domains where user traits strongly influence interaction quality.

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
pip install tau-trait
```

## Usage

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

## Tau-Hard Config Settings
### General
- **`--num-trials`** *(int, default: 1)*  
  Number of independent trials to run.

- **`--seed`** *(int, default: 10)*  
  Random seed for reproducibility.

- **`--shuffle`** *(int, default: 0)*  
  Whether to shuffle task order (0 = no, 1 = yes).

- **`--log-dir`** *(str, default: `results`)*  
  Directory where logs and results are stored.

### Environment & Tasks
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

### Agent Configuration
- **`--model`** *(str, required)*  
  The model to use for the **agent**.

- **`--model-provider`** *(str, choices from `provider_list`)*  
  Provider for the agent’s model.

- **`--agent-strategy`** *(str, choices: `tool-calling`, `act`, `react`, `few-shot`, default: `tool-calling`)*  
  Strategy used by the agent to interact with the environment.  
  - `tool-calling`: Invoke external tools.  
  - `act`: Pure action selection.  
  - `react`: Reason + act alternation.  
  - `few-shot`: Use few-shot exemplars.

- **`--temperature`** *(float, default: 0.0)*  
  Sampling temperature for the action model (higher = more randomness).

- **`--few-shot-displays-path`** *(str, optional)*  
  Path to a JSONL file containing few-shot demonstration examples.

### User Simulator Configuration
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