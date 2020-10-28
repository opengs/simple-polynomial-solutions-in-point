from .algorithm import Algorithm

class Result():
    def __init__(self, algorithm: Algorithm, solution: float, multiply_count: int, addition_count: int) -> None:
        self.algorithm = algorithm
        self.solution = solution
        self.multiply_count = multiply_count
        self.addition_count = addition_count

    @property
    def total_operations(self) -> int:
        return self.multiply_count + self.addition_count

    def print(self):
        print(f"Algorithm: {self.algorithm.name}")
        print(f"Solution: {self.solution}")
        print(f"Multiply operations: {self.multiply_count}")
        print(f"Add operations: {self.addition_count}")
        print()
