from constraint import AlldiffConstraint, LeadingZeroConstraint, TotalConstraint
from utils import *
from poland import infix_to_postfix
class CryptarithmeticProblem:
    
    def __init__(self, equation):
        self.variables, self.domains, self.operands, self.expression, self.result = parse_input(equation)
        self.postfix_expression = infix_to_postfix(self.expression)
        self.constraints = [
            AlldiffConstraint(self.variables, self.domains),
            TotalConstraint(self.variables, self.domains, self.postfix_expression, self.result),
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

        var = self.get_next_variable(unassigned_vars)
        for value in self.get_ordered_values(var, assignment):
            assignment[var] = value
            if self.is_value_consistent(assignment):
                result = self.solve_cryptarithmetic(assignment)
                if result:
                    return result
            del assignment[var]

        return None

    def get_next_variable(self, unassigned_vars):
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