from typing import List

from .algorithm import Algorithm
from .result import Result

class GournerPower2(Algorithm):
    @property
    def name(self) -> str:
        return f"Multithread Gourner power 2"

    def _gourner_rec(self, coefitients: List[float], value: float) -> Result:
        if len(coefitients) == 0:
            return Result(self, 0, 0, 0)

        if len(coefitients) == 1:
            return Result(self, coefitients[0], 0, 0)

        if len(coefitients) == 2:
            return Result(self, coefitients[0] + coefitients[1]*value, 1, 1)

        even = coefitients[0::2]
        odd = coefitients[1::2]

        #TODO: run this in thread pool
        even_result = self._gourner_rec(even, value*value)
        odd_result = self._gourner_rec(odd, value*value)

        return Result(
            self,
            even_result.solution + odd_result.solution * value,
            even_result.multiply_count + odd_result.multiply_count + 1,
            even_result.addition_count + odd_result.addition_count + 1
        )

    def solve(self, coefitients: List[float], value: float) -> Result:
        coefitients.reverse()
        return self._gourner_rec(coefitients, value)