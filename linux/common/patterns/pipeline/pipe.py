from abc import ABC, abstractmethod
from typing import Any

class IPipe(ABC):
    @abstractmethod
    def flow(self, data: Any) -> Any:
        """
        Process the data and return the result.
        """
        pass
