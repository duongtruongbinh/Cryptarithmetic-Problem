import constraint


class CryptarithmeticProblem:
    def __init__(self, filepath: str):
        self.equation = self.read_file(filepath)
        self.variables, self.words, self.operators = self.parse_input()
        self.domain = {var: [i for i in range(10)] for var in self.variables}
        self.constraints = [
            constraint.AlldiffConstraint(self.variables),
            constraint.TotalConstraint(self.variables, self.words),
            constraint.LeadingZeroConstraint(self.variables, self.words)
        ]

    def read_file(self, filepath: str) -> str:
        with open(filepath, 'r') as file:
            equation = file.readline()
        return equation

    def write_file(self, filepath, solution) -> None:
        with open(filepath, 'w') as file:
            if solution:
                vars = sorted(solution.keys())
                for var in vars:
                    file.write(str(solution[var]))
            else:
                file.write("NO SOLUTION")

    def normalize_equation(self, equation: str) -> str:
        result = []
        inside_parentheses = False

        for char in equation:
            if char.isalpha():
                result.append(char)
            elif char == '(':
                inside_parentheses = result and result[-1] == '-'
            elif char == ')':
                inside_parentheses = False
            elif inside_parentheses:
                result.append('-' if char == '+' else '+')
            else:
                result.append(char)

        return ''.join(result)

    def parse_input(self) -> tuple[list[str], list[str], list[str]]:
        self.equation = self.normalize_equation(self.equation)
        print(self.equation)
        variables = []
        words = []
        operators = []
        word = ''
        if self.equation[0] == '-':
            operators.append('-')
            self.equation = self.equation[1:]
        elif self.equation[0].isalpha():
            operators.append('+')

        for i in range(len(self.equation)):
            if self.equation[i] == '+':
                if self.equation[i+1] == '-':
                    operators.append('-')
                    words.append(word)
                elif self.equation[i+1].isalpha() and self.equation[i-1].isalpha():
                    operators.append('+')
                    words.append(word)
                word = ''
                continue
            elif self.equation[i] == '-':
                if self.equation[i+1] == '-':
                    operators.append('+')
                    words.append(word)
                elif self.equation[i+1].isalpha() and self.equation[i-1].isalpha():
                    operators.append('-')
                    words.append(word)
                word = ''
                continue
            elif self.equation[i] == '=':
                if self.equation[i+1] == '-':
                    operators.append('-')

                elif self.equation[i+1].isalpha():
                    operators.append('+')
                words.append(word)
                word = ''
                continue

            elif self.equation[i].isalpha():
                word += self.equation[i]
                variables.append(self.equation[i])
        words.append(word)

        return set(variables), words, operators

    def solve(self) -> dict[str, int]:
        for constraint in self.constraints:
            constraint.preProcess(self.domain)

        solution = self.solve_cryptarithmetic({})
        return solution

    def solve_cryptarithmetic(self, assignment: dict[str, int]) -> dict[str, int]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned_vars = [
            var for var in self.variables if var not in assignment]

        var = self.get_next_variable(unassigned_vars)
        for value in self.get_ordered_values(var, assignment):
            assignment[var] = value
            if self.is_value_consistent(assignment):
                result = self.solve_cryptarithmetic(assignment)
                if result:
                    return result
            del assignment[var]

        return None

    def get_next_variable(self, unassigned_vars: list[str]) -> str:
        # MRV heuristic: Choose the variable with the fewest remaining values in its domain.
        return min(unassigned_vars, key=lambda var: len(self.domain[var]))

    def get_ordered_values(self, var: str, assignment: dict[str, int]) -> list[int]:
        # LCV heuristic: Order the domain values based on the least constraining values.
        values = self.domain[var]
        return sorted(values, key=lambda value: self.count_conflicts(var, value, assignment))

    def count_conflicts(self, var: str, value: int, assignment: dict[str, int]) -> int:
        conflicts = 0
        for constraint in self.constraints:
            if var in constraint.variables and not constraint.satisfied({**assignment, var: value}):
                conflicts += 1
        return conflicts

    def is_value_consistent(self, assignment: dict[str, int]) -> bool:
        for constraint in self.constraints:
            if not constraint.satisfied(assignment):
                return False
        return True
