from constraint import AlldiffConstraint, LeadingZeroConstraint
from functools import reduce
from utils import normalize_equation, split_equation, create_subproblem

class CryptarithmeticProblem:
    def __init__(self, equation):
        self.equation = normalize_equation(equation)
        self.variables, self.operators, self.operands, self.result = split_equation(self.equation)
        self.domains = {var: [i for i in range(10)] for var in self.variables}
        self.constraints = [
            LeadingZeroConstraint(self.variables, self.domains, self.operands, self.result),
            AlldiffConstraint(self.variables, self.domains)
        ]
        self.subproblems, self.impact = create_subproblem(self.operands, self.operators, self.result)

    def all_assigned(self):
        return all(variable is not None for variable in self.variables)
    
    def check_subproblem(self, subproblem, impact, carry):
        total = 0
        for char in subproblem:
            total += ((-1)**impact[char]) *  self.variables[char]
        total += carry

        if total % 10 != 0:
            return None

        return total / 10

    def solve_subproblem(self, subproblem, impact, charIndex, spIndex, carry):
        if charIndex == len(subproblem):
            new_carry = self.check_subproblem(subproblem, impact, carry)
            return self.backtracking_search(spIndex + 1, new_carry) if new_carry is not None else None

        char = subproblem[charIndex]

        if self.variables[char] is None:
            current_domain = self.domains[char].copy()
        
            common_domain = reduce(set.intersection, (set(c.satisfied(char)) for c in self.constraints))
            self.domains[char] = list(common_domain)
            # print(self.domains[char])

            for val in self.domains[char]:
                self.variables[char] = val
                assign = self.solve_subproblem(subproblem, impact, charIndex + 1, spIndex, carry)
                if assign is not None:
                    return assign
            
            self.variables[char] = None
            self.domains[char] = current_domain
        else:
            return self.solve_subproblem(subproblem, impact, charIndex + 1, spIndex, carry)

    def is_consistent(self):
        carry = 0
        for subproblem, impact in zip(self.subproblems, self.impact):
            carry = self.check_subproblem(subproblem, impact, carry)
            if carry is None:
                return False
        return carry == 0

    def backtracking_search(self, index=0, carry=0):
        if len(self.variables) > 10:
            return None 

        if index == len(self.subproblems):
            return self.variables if carry == 0 else None

        return self.solve_subproblem(self.subproblems[index], self.impact[index], 0, index, carry)
    