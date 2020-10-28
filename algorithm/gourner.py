from typing import List

from .algorithm import Algorithm
from .result import Result

class Gourner(Algorithm):
    def __init__(self, gourner_power: int = 1) -> None:
        self._gourner_power = gourner_power

    @property
    def name(self) -> str:
        return f"Gourner (power {self._gourner_power})"

    def _gourner_rec(self, coefitients: List[float], value: float) -> Result:
        if len(coefitients) == 0:
            return Result(self, 0, 0, 0)

        if len(coefitients) == self._gourner_power:
            return Result(self, coefitients[-1], 0, 0)

        rec_result = self._gourner_rec(coefitients[:-self._gourner_power], value)
        rec_result.solution = rec_result.solution * value + coefitients[-1]
        rec_result.addition_count += 1
        rec_result.multiply_count += 1

        return rec_result

    def solve(self, coefitients: List[float], value: float) -> Result:
        return self._gourner_rec(coefitients, value ** self._gourner_power)