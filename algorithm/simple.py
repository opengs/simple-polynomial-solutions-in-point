from typing import List

from .algorithm import Algorithm
from .result import Result

class Simple(Algorithm):
    @property
    def name(self) -> str:
        return "Simple"

    def solve(self, coefitients: List[float], value: float) -> Result:
        solution = 0
        additions_count = 0
        multiply_count = 0
        
        power = len(coefitients)

        for cf_index in range(len(coefitients)):
            # Manual power loop
            value_to_power = 1
            for i in range(power - cf_index - 1):
                multiply_count += 1
                value_to_power *= value

            solution += coefitients[cf_index] * value_to_power
            multiply_count += 1
            additions_count += 1

        return Result(self, solution, multiply_count, additions_count)