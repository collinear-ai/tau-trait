<p align="center">
  <img src="assets/collinear.png" width="200"/>
</p>

# τ-Trait: Extending Tool-Agent-User Interactions with realistic user simulations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &nbsp; &nbsp; [![arXiv](https://img.shields.io/badge/arxiv-2510.04491-b31b1b)](https://arxiv.org/abs/2510.04491) &nbsp; &nbsp; [![Blog:TraitBasis](https://img.shields.io/badge/Blog-TraitBasis-orange)](https://blog.collinear.ai/p/trait-basis) &nbsp; &nbsp; [![Notebook:simulations](https://img.shields.io/badge/Notebook-simulations-blue)](https://github.com/collinear-ai/simulations)

**$\tau$-Trait** is a benchmark for evaluating large language models (LLMs) with **realistic, persona-aware simulations**. It builds on $\tau$-Bench but introduces two key modifications:

1. **TraitBasis-generated personas** – more accurate and interpretable user simulations.
2. **Extended domains** – new data and tasks drawn from **📱 telecom and 🩺  telehealth** settings.

$\tau$-Trait is designed to test model **robustness, personalization, and fairness** in high-impact, customer-facing domains where user traits strongly influence interaction quality.

## Results  
Drops in agent performance with user simulations with TraitBasis relative to without any traits, averaged across 3 runs.

| Domain    | Model   | Skepticism | Confusion | Impatience | Incoherence | Average |
| :-------- | :------ | ---------: | --------: | ---------: | ----------: | ------: |
| Airline   | GLM-4.5 |     -11.0% |    -16.9% |     -12.8% |      -12.2% |  -13.2% |
|           | GPT-4o  |      -6.7% |     -5.0% |      -4.4% |       -6.7% |   -5.7% |
|           | Kimi K2 |     -11.8% |     -9.5% |      -6.2% |       -7.1% |   -8.7% |
| Retail    | GLM-4.5 |       0.2% |     -5.4% |      -2.6% |       -0.5% |   -2.1% |
|           | GPT-4o  |     -29.2% |    -34.2% |     -25.9% |      -22.9% |  -28.1% |
|           | Kimi K2 |     -21.9% |    -45.7% |     -31.2% |      -21.4% |  -30.0% |
| Telecom   | GLM-4.5 |       0.8% |    -16.8% |      -3.9% |       -2.3% |   -5.5% |
|           | GPT-4o  |     -11.5% |    -14.0% |     -16.9% |       -8.7% |  -12.8% |
|           | Kimi K2 |     -11.4% |    -18.1% |     -14.7% |       -4.5% |  -12.2% |


## 🚀 Getting Started

### Setup

1. Clone this repository:

```bash
git clone https://github.com/collinear-ai/tau-trait && cd ./tau-trait
```

2. Install from source along with other required packages:

```bash
conda create -n tau_trait -y python=3.11
conda activate tau_trait
pip install jupyterlab ipykernel nest_asyncio jinja2 --no-cache
pip install "openai>=1.13.3" "mistralai>=0.4.0" "anthropic>=0.26.1" "google-generativeai>=0.5.4" "tenacity>=8.3.0" "termcolor>=2.4.0" "numpy>=1.26.4" "litellm==1.41.0"
pip install -e .
```

3. Set up your steer API key (for the user model) and your OpenAI / Anthropic / Google / Mistral / AnyScale API keys (for the assistant model) as environment variables. Note: if you do not have a steer API key, you can use **tautrait-001** for non-production workloads. Please reach out if you are interested in your own API key for optimized inference and throughput. 

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
STEER_API_KEY=...
```


## Usage

### Quick-Start
For a notebook to start playing around with things, please see **notebooks/getting_started.ipynb**

### CLI commands 

```
python run.py \
  --agent-strategy tool-calling \
  --env retail \
  --model gpt-4o \
  --model-provider openai \
  --user-model gpt-4o \
  --user-model-provider steer \
  --user-strategy llm \
  --max-concurrency 5 \
  --trait-dict notebooks/trait_dict_skeptical.json \
  --result-fp notebooks/results/test.json \
  --endpoint https://steer.collinear.ai/steer_bare
```

Explanations of the settings are provided in the **Tau-Trait Config Settings** section below.


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

- **`--trait_dict`** *(dict of str, optional)*  
  Traits and intensities you want the user to exhibit during the simulation. 

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


## τ-Trait vs τ-Bench rollouts 

![Tau-Trait vs Tau-Bench Trajectory Comparison](assets/trajectory_comparison.png)

---


```
@article{he2025impatient,
  title        = {Impatient Users Confuse AI Agents: High-fidelity Simulations of Human Traits for Testing Agents},
  author       = {He, Muyu and Kumar, Anand and Mackey, Tsach and Rajeev, Meghana and Zou, James and Rajani, Nazneen},
  journal      = {arXiv preprint arXiv:2510.04491},
  year         = {2025},
  url          = {https://arXiv.org/abs/2510.04491}
}
```
