from abc import ABC, abstractmethod


class Constraint(ABC):
    def __init__(self, variables: list[str]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: dict[str, int]):
        return True

    @abstractmethod
    def preProcess(self, domains: dict[str, list[int]]):
        return


class AlldiffConstraint(Constraint):
    def __init__(self, variables: list[str]):
        super().__init__(variables)

    def preProcess(self, domains: dict[str, list[int]]):
        for var in self.variables:
            if len(domains[var]) == 1:
                assigned_value = domains[var][0]
                for other_var in self.variables:
                    if other_var != var and assigned_value in domains[other_var]:
                        domains[other_var].remove(assigned_value)

    def satisfied(self, assignment: dict[str, int]) -> bool:
        assigned = set(assignment.values())
        return len(assigned) == len(assignment)


class TotalConstraint(Constraint):
    def __init__(self, variables: list[str], words: list[str]):
        super().__init__(variables)
        self.words = words

    def preProcess(self, domains: dict[str, list[int]]):
        # Perform any pre-processing for the SumConstraint if required.
        pass

    def satisfied(self, assignment: dict[str, int]) -> bool:
        if len(assignment) != len(self.variables):
            return True

        word_values = []
        for i in range(len(self.words)):
            word_value = 0
            for letter in self.words[i]:
                word_value *= 10
                word_value += assignment[letter]

            word_values.append(
                word_value*(-1) if self.words[i][0] == '-' else word_value)

        return sum(word_values[:-1]) == word_values[-1]


class LeadingZeroConstraint(Constraint):
    def __init__(self, variables: list[str], words: list[str]):
        super().__init__(variables)
        self.leading_letters = [word[0] for word in words if len(word) > 1]

    def preProcess(self, domains: dict[str, list[int]]):
        for letter in self.leading_letters:
            if 0 in domains[letter]:
                domains[letter].remove(0)

    def satisfied(self, assignment):
        return True
