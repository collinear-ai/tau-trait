
from typing import Optional, Union, Dict
from tau_trait.envs.base import Env
from tau_trait.envs.user import UserStrategy


def get_env(
    env_name: str,
    user_strategy: Union[str, UserStrategy],
    user_model: str,
    task_split: str,
    user_provider: Optional[str] = None,
    task_index: Optional[int] = None,
    trait_dict: Optional[Dict[str, int]] = None,
    endpoint: Optional[str] = None,
) -> Env:

    if env_name == "retail":
        from tau_trait.envs.retail import MockRetailDomainEnv

        return MockRetailDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            trait_dict=trait_dict,
            endpoint=endpoint,
        )
    elif env_name == "airline":
        from tau_trait.envs.airline import MockAirlineDomainEnv

        return MockAirlineDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            trait_dict=trait_dict,
            endpoint=endpoint,
        )
    elif env_name == "telecom":
        from tau_trait.envs.telecom import MockTelecomDomainEnv

        return MockTelecomDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            trait_dict=trait_dict,
            endpoint=endpoint,
        )
    elif env_name == "telehealth":
        from tau_trait.envs.telehealth import MockTelehealthDomainEnv

        return MockTelehealthDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            trait_dict=trait_dict,
            endpoint=endpoint,
        )
    else:
        raise ValueError(f"Unknown environment: {env_name}")
