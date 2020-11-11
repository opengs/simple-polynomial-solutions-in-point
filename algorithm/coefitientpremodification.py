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
        g2 = x*(x+c[1]) # M 1, A 1
        h2 = g2 + x # M 1, A 2
        i2 = h2 + x # M 1, A 3

        p4 = lambda: (g2 + c[2]) * (h2 + c[3]) + c[4] # M 1 A 2 (h2|g2) + M 1 A 3 = M 4 A 5
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
            4: lambda: ql(4), # M 5, A 5
            5: lambda: qm(5), # M 6, A 6
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
        output.append(0.5*(c[1]/c[0] - 1)) # M 2, A 1
        l1 = output[1]
        l1l1 = l1*l1 # M 1, A 0

        output.append(c[3]/c[0] - l1*c[2]/c[0] + l1l1*(l1 + 1)) # M 4, A 3
        output.append(c[2]/c[0] - l1*(l1+1) - output[2]) # M 2, A 3
        output.append(c[4]/c[0] - output[2]*output[3]) # M 2, A 1

        if len(c) == 6:
            output.append(c[5])

        # Total transformation operations: M(multiply) 11, A(add) 8
        return output

    def _transform_coefitients(self, c: List[float]) -> List[float]:
        ln = len(c)
        if ln != 5 and ln != 6:
            raise NotSupportedPowerException()

        return self._transform45(c)

    def _transformation_cost(self, c: List[float]):
        ln = len(c) - 1
        if ln == 4:
            return 11, 8
        elif ln == 5:
            return 11, 8
        
        raise NotSupportedPowerException()

    def _solving_cost(self, c: List[float]):
        ln = len(c) - 1
        if ln == 4:
            return 5, 5
        elif ln == 5:
            return 6, 6
        
        raise NotSupportedPowerException()

    def _cost(self, c: List[float]):
        t_m, t_a = self._transformation_cost(c)
        s_m, s_a = self._solving_cost(c)

        return t_m + s_m, t_a + s_a

    def solve(self, coefitients: List[float], value: float) -> Result:
        try:
            coefitients = self._transform_coefitients(coefitients)
            solvers = self._get_solvers(coefitients, value)
            solution_number = len(coefitients) - 1
            if solution_number not in solvers:
                raise NotSupportedPowerException()
            solver = solvers[solution_number]

            multiplies, adds = self._cost(coefitients)

            return Result(self, solver(), multiplies, adds)
        except NotSupportedPowerException:
            return Result(self, 0, 0, 0, "Incompatible number of coefitients.")  