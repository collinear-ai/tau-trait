#!/usr/bin/env python3

import subprocess
import sys
import os

import argparse 
import json 

def load_model_configs(config_files): 
    """Load model configurations from a list of JSON files."""
    models = []
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                models.append(config)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file {config_file}: {e}")
            sys.exit(1)
    return models

def load_eval_configs(eval_config_file):
    try: 
        with open(eval_config_file, "r") as f: 
            eval_configs = json.load(f)
        return eval_configs
    except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading eval config file {eval_config_file}: {e}")
            sys.exit(1)

def get_eval_configs(starting_run_id, starting_fine_grained_eval_id, num_runs, envs, trait_dicts, models, task_ids):
    """
    Generate evaluation configurations for all combinations of runs, environments, trait dictionaries, and models.

    Args:
        starting_run_id (int): The starting index for run IDs.
        starting_fine_grained_eval_id (int): The starting index for fine-grained evaluation IDs.
        num_runs (int): The total number of runs to generate.
        envs (list): List of environment names.
        trait_dicts (list): List of trait dictionary names.
        models (list): List of model configuration dictionaries.
        task_ids (list): List of task ids to do the evaluation over 

    Returns:
        list: A list of dictionaries, each representing a unique evaluation configuration.
    """
    run_configs = []
    fine_grained_eval_id = 0 
    for run_id in range(starting_run_id, num_runs):
        for env in envs:
            for trait_dict in trait_dicts:
                # Loop through all combinations of environments and trait dictionaries
                for model in models:

                    if starting_fine_grained_eval_id and fine_grained_eval_id < starting_fine_grained_eval_id: 
                        fine_grained_eval_id += 1
                        continue
                    
                    run_configs.append(
                        {
                            "run_id": run_id,
                            "env": env,
                            "trait_dict": trait_dict,
                            "model": model,
                            "task_ids": task_ids
                        }
                    )
    return run_configs 
    
def run_evaluation(results_folder, starting_run_id=0, models=None, eval_configs = None):
    user_model = "gpt-4o"
    user_model_provider = "steer"
    # make results folder if it doesn't exist
    if not os.path.exists(f"results/{results_folder}"):
        os.makedirs(f"results/{results_folder}")
        
    if not eval_configs: 
        # Use a few default values 
        envs = ["retail"]
        trait_dicts = ["trait_dict_skeptical", "trait_dict_impatient"]
        task_ids = None
        starting_fine_grained_eval_id = 0
        num_runs = 3

        eval_configs = get_eval_configs(starting_run_id, starting_fine_grained_eval_id, num_runs, envs, trait_dicts, models, task_ids)

    for eval_config in eval_configs: 
        model = eval_config["model"]
        env = eval_config["env"]
        trait_dict = eval_config["trait_dict"]
        run_id = eval_config["run_id"]
        task_ids = eval_config["task_ids"]
        
        model_name = model["name"]
        model_provider = model["provider"]
        model_model = model["model"]
        max_concurrency = model["max_concurrency"]
        print(f"Running evaluation for env: {env}, trait-dict: {trait_dict} with model: {model_name}")
        fp = f"results/{results_folder}/{model_name}_{env}_{trait_dict}_{run_id}.json"
        common_args = [
            "python", "run.py",
            "--agent-strategy", "tool-calling",
            "--env", env,
            "--model", model_model,
            "--model-provider", model_provider,
        ]
        if trait_dict == "none":
            cmd = common_args + [
                "--user-model", "gpt-4o",
                "--user-model-provider", "openai",
                "--user-strategy", "llm",
                "--max-concurrency", str(max_concurrency),
                "--result-fp", fp,
            ]
        else:                     
            
            cmd = common_args + [
                "--user-model", user_model,
                "--user-model-provider", user_model_provider,
                "--user-strategy", "llm",
                "--max-concurrency", str(max_concurrency),
                "--trait-dict", f"eval_scripts/{trait_dict}.json",
                "--result-fp", fp,
                "--endpoint", "https://steer.collinear.ai/steer_bare"
            ]
        if task_ids is not None:
            cmd += ["--task-ids"] + list(map(str, task_ids))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running evaluation for {env} with {trait_dict}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run evaluations with specified model configurations")
    parser.add_argument(
        "--model-configs", 
        nargs='+', 
        default=None,
        help="List of JSON config files for models to evaluate"
    )
    parser.add_argument(
        "--starting_run_id",  
        default=0,
        help="Trial index at which to start the eval. Defaults to 0"  
    )
    parser.add_argument(
        "--eval_config_file",
        default = None, 
        help="Config file with all of the evals"
    )
    parser.add_argument(
        "--results_folder",
        help="Folder to store the trajectories"
    )

    args = parser.parse_args()
    
    if args.eval_config_file:   
        eval_configs = load_eval_configs(args.eval_config_file)
        run_evaluation(args.results_folder, starting_run_id=int(args.starting_run_id), eval_configs=eval_configs)
    else: 
        models = load_model_configs(args.model_configs)
        run_evaluation(args.results_folder, starting_run_id=int(args.starting_run_id), models=models)

    
