from abc import ABC, abstractmethod
from typing import Any, Dict


class QueryBuilder(ABC):
    """
    abstract class for query builders,
        sub_classes will return query string
    """

    @abstractmethod
    def query_create(self, class_name: str, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def query_update(self, rid: str, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def query_delete(self, rid: str) -> str:
        pass

    @abstractmethod
    def query_retrieve(self, *args, **kwargs) -> str:
        pass
