import abc
from typing import Any, Dict


class Tool(abc.ABC):
    @staticmethod
    def invoke(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_info() -> Dict[str, Any]:
        raise NotImplementedError
