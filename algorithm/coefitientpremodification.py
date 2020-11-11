from typing import List

from .algorithm import Algorithm
from .result import Result

class NotSupportedPowerException(Exception):
    pass

class CoefitientPreModification(Algorithm):
    @property
    def name(self) -> str:
        return "Coefitient pre modification"

    def _get_solvers(self, c: List[float], x: float):
        g2 = x*(x+c[1])
        h2 = g2 + x
        i2 = h2 + x

        p4 = lambda: (g2 + c[2]) * (h2 + c[3]) + c[4]
        p6 = lambda: ((g2 + c[2]) * (i2 + c[3]) + c[4]) * (h2 + c[5]) + c[6]
        p8 = lambda: p6()*(g2 + c[7]) + c[8]
        p11 = lambda: (x * p8() + c[9])(i2 + c[10]) + c[11]
        p_dict = {
            4: p4,
            6: p6,
            8: p8,
            11: p11
        }

        ql = lambda l: c[0] * p_dict[l]() # l є {4, 6, 8, 11}
        qm = lambda m: c[0] * x * p_dict[m-1]() + c[m] # m є {5, 7, 9, 12}
        q10 = lambda: x * (c[0] * x * p8() + c[9]) + c[10]

        return {
            4: lambda: ql(4),
            5: lambda: qm(5),
            6: lambda: ql(6),
            7: lambda: qm(7),
            8: lambda: ql(8),
            9: lambda: qm(9),
            10: q10,
            11: lambda: ql(11),
            12: lambda: qm(12),
        }    

    def _transform45(self, c: List[float]):
        output: List[float] = []
        output.append(c[0])
        output.append(0.5*(c[1]/c[0] - 1))
        l1 = output[1]
        l1l1 = l1*l1

        output.append(c[3]/c[0] - l1*c[2]/c[0] + l1l1*(l1 + 1))
        output.append(c[2]/c[0] - l1*(l1+1) - output[2])
        output.append(c[4]/c[0] - output[2]*output[3])

        if len(c) == 6:
            output.append(c[5])

        return output

    def _transform_coefitients(self, c: List[float]) -> List[float]:
        ln = len(c)
        if ln != 5 and ln != 6:
            raise NotSupportedPowerException()

        return self._transform45(c)

    def solve(self, coefitients: List[float], value: float) -> Result:
        try:
            coefitients = self._transform_coefitients(coefitients)
            solvers = self._get_solvers(coefitients, value)
            solution_number = len(coefitients) - 1
            if solution_number not in solvers:
                raise NotSupportedPowerException()
            solver = solvers[solution_number]
            return Result(self, solver(), -1, -1)
        except NotSupportedPowerException:
            return Result(self, 0, 0, 0, "Incompatible number of coefitients.")  