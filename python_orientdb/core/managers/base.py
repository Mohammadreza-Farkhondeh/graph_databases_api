from abc import ABC, abstractmethod
from typing import Any, Dict

class Manager(ABC):
    """
    abstract class for managers
        sub_classes will use query_builder to execute queries on orientdb
    """

    @abstractmethod
    async def create(self, class_name: str, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def update(self, rid: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def delete(self, rid: str) -> bool:
        pass

    @abstractmethod
    async def retrieve(self, filters: Dict[str, Any]) -> Any:
        pass
