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
    model="gpt-4o",
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
    user_strategy="llm",
    few_shot_displays_path=None,
    trait_dict={"impatience": 1, "confusion": 0, "skeptical": 0, "incoherence": 0},
)