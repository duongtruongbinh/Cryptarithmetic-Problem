from abc import ABC, abstractmethod
from collections import defaultdict

class Constraint(ABC):
    def __init__(self, variables: dict, domains: defaultdict[list]):
        self.variables = variables
        self.domains = domains
    
    @abstractmethod
    def satisfied(self, char: str) -> list:
        return

class LeadingZeroConstraint(Constraint):
    def __init__(self, variables: dict, domains: defaultdict[list], operands: list, result: str):
        super().__init__(variables, domains)
        self.leading_letters = [operand[0] for operand in operands if len(operand) > 1] + ([result[0]] if len(result) > 1 else [])

    def satisfied(self, char: str) -> list:
        domain = self.domains[char].copy()
        if char in self.leading_letters and 0 in domain:
            domain.remove(0)
        return domain

class AlldiffConstraint(Constraint):
    def __init__(self, variables: dict, domains: defaultdict[list]):
        super().__init__(variables, domains)
        
    def satisfied(self, char: str) -> list:
        domain = self.domains[char].copy()
        for var in self.variables:
            if var != char and self.variables[var] in domain:
                domain.remove(self.variables[var])
        return domain