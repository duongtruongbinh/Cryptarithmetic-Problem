from abc import ABC, abstractmethod
from poland import evaluate_prefix
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
    def __init__(self, variables, domains, prefix_expression, result):
        super().__init__(variables, domains)
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
        left_side = evaluate_prefix(operand_values)
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