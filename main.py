from typing import List

from algorithm.algorithm import Algorithm
from algorithm.simple import Simple
from algorithm.simpleextended import SimpleExtended
from algorithm.gourner import Gourner
from algorithm.coefitientpremodification import CoefitientPreModification

from importer import ImportedData, ImportException, import_from_file

def main():
    # Importing data
    try:
        input = import_from_file("data.json")
    except ImportException as e:
        print(e)
        return
    
    # Accumulating algorithms
    algorithms: List[Algorithm] = []
    algorithms.append(Simple())
    algorithms.append(SimpleExtended())
    algorithms.append(Gourner())
    algorithms.append(Gourner(2))
    algorithms.append(CoefitientPreModification())

    # Solve and print
    for alg in algorithms:
        result = alg.solve(input.coefitients, input.value)
        result.print()

if __name__ == "__main__":
    main()