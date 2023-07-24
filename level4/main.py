import re
from abc import ABC, abstractmethod
import copy
from utils import normalize_equation, parse_input
from poland import tokenize_expression, infix_to_prefix, evaluate

class CryptarithmeticProblem:
    def __init__(self, equation):
        self.equation = normalize_equation(equation)
        self.variables, self.domains, self.operators, self.operands, self.result = parse_input(self.equation)
        self.prefix_expression = infix_to_prefix(tokenize_expression(equation))
        self.constraints = [
            AlldiffConstraint(self.variables, self.domains),
            TotalConstraint(self.variables, self.domains, self.operands, self.operators, self.result, self.prefix_expression),
            LeadingZeroConstraint(self.variables, self.domains, self.operands, self.result)
        ]
        self.pre_process_constraints()

    def pre_process_constraints(self):
        for constraint in self.constraints:
            if constraint.pre_process():
                self.constraints.remove(constraint)

    def solve_cryptarithmetic(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned_vars = [var for var in self.variables if var not in assignment]

        var = self.get_next_variable(assignment, unassigned_vars)
        for value in self.get_ordered_values(var, assignment):
            assignment[var] = value
            if self.is_value_consistent(assignment):
                result = self.solve_cryptarithmetic(assignment)
                if result:
                    return result
            del assignment[var]

        return None

    def get_next_variable(self, assignment, unassigned_vars):
        # MRV heuristic: Choose the variable with the fewest remaining values in its domain.
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def get_ordered_values(self, var, assignment):
        # LCV heuristic: Order the domain values based on the least constraining values.
        values = self.domains[var]
        return sorted(values, key=lambda value: self.count_conflicts(var, value, assignment))

    def count_conflicts(self, var, value, assignment):
        conflicts = 0
        for constraint in self.constraints:
            if var in constraint.variables:
                if not constraint.satisfied({var: value, **assignment}):
                    conflicts += 1
        return conflicts

    def is_value_consistent(self, assignment):
        for constraint in self.constraints:
            if not constraint.satisfied(assignment):
                return False
        return True


class Constraint(ABC):
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains

    @abstractmethod
    def satisfied(self, assignment):
        return True

    @abstractmethod
    def pre_process(self):
        return


class AlldiffConstraint(Constraint):
    def __init__(self, variables, domains):
        super().__init__(variables, domains)

    def pre_process(self):
        for var in self.variables:
            if len(self.domains[var]) == 1:
                assigned_value = self.domains[var][0]
                for other_var in self.variables:
                    if other_var != var and assigned_value in self.domains[other_var]:
                        self.domains[other_var].remove(assigned_value)

    def satisfied(self, assignment):
        assigned = set(assignment.values())
        return len(assigned) == len(assignment)


class TotalConstraint(Constraint):
    def __init__(self, variables, domains, operands, operators, result, prefix_expression):
        super().__init__(variables, domains)
        self.operands = operands
        self.operators = operators
        self.result = result
        self.prefix_expression = prefix_expression

    def pre_process(self):
        # Perform any pre-processing for the TotalConstraint if required.
        pass

    def satisfied(self, assignment):
        if len(assignment) != len(self.variables):
            return True

        operand_values = []
        for element in self.prefix_expression:
            if not element.isalpha():
                operand_values.append(element)
                continue
            result = ''.join(str(assignment[c]) for c in element)
            operand_values.append(result)
        # print(operand_values)
        left_side = evaluate(operand_values)
        right_side = int(''.join(str(assignment[c]) for c in self.result))
        return left_side == right_side


class LeadingZeroConstraint(Constraint):
    def __init__(self, variables, domains, operands, result):
        super().__init__(variables, domains)
        self.leading_letters = [operand[0] for operand in operands if len(operand) > 1] + [result[0]]

    def pre_process(self):
        for letter in self.leading_letters:
            if 0 in self.domains[letter]:
                self.domains[letter].remove(0)

    def satisfied(self, assignment):
        return True

# equation = 'APD*AD=DPCED'
equation = 'HE*EH=HNME'
problem = CryptarithmeticProblem(equation)
print(problem.prefix_expression)
solution = problem.solve_cryptarithmetic({})

if solution:
    print(solution)
    vars = sorted(solution.keys())
    for var in vars:
        print(solution[var], end='')
else:
    print("No solution found.")
# total = TotalConstraint(problem.variables, problem.domains, problem.operands, problem.operators, problem.result, problem.prefix_expression)

# solution = {'S': 8, 'E': 2, 'N': 6, 'D': 1, 'M': 5, 'O': 3, 'R': 0, 'Y': 4, 'I': 9, 'U': 7}
# print(total.satisfied(solution))