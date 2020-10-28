from abc import ABC, abstractmethod
from typing import List

class Algorithm(ABC):
    pass
    
from .result import Result

class Algorithm(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def solve(self, coefitients: List[float], value: float) -> Result:
        pass