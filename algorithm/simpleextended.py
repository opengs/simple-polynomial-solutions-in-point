from typing import List

from .algorithm import Algorithm
from .result import Result

class SimpleExtended(Algorithm):
    @property
    def name(self) -> str:
        return "Simple (extended)"

    def solve(self, coefitients: List[float], value: float) -> Result:
        solution = 0
        additions_count = 0
        multiply_count = 0
        
        power = len(coefitients)

        # cache power
        power_cahe: List[float] = []
        power_cahe.append(1)
        value_to_power = 1
        for cf_index in range(power-1):
            multiply_count += 1
            value_to_power *= value
            power_cahe.append(value_to_power)

        for cf_index in range(len(coefitients)):
            solution += coefitients[cf_index] * power_cahe[power - cf_index - 1]
            multiply_count += 1
            additions_count += 1

        return Result(self, solution, multiply_count, additions_count)