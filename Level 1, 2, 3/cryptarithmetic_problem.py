from constraint import AlldiffConstraint, LeadingZeroConstraint
from functools import reduce
from utils import normalize_equation, parse_input, create_subproblem, read_file

class CryptarithmeticProblem:
    def __init__(self, file_path):
        self.equation = normalize_equation(read_file(file_path))
        self.variables, self.domains, self.operators, self.operands, self.result = parse_input(self.equation)
        self.constraints = [
            LeadingZeroConstraint(self.variables, self.domains, self.operands, self.result),
            AlldiffConstraint(self.variables, self.domains)
        ]
        self.subproblems, self.impact = create_subproblem(self.operands, self.operators, self.result)
        #preProcess
        self.pre_process_constraints()

    def pre_process_constraints(self):
        for constraint in self.constraints:
            if constraint.preProcess():
                self.constraints.remove(constraint)
    
    def check_subproblem(self, subproblem, impact, carry):
        total = sum(self.variables[char] * impact[char] for char in subproblem) + carry
        return total / 10 if total % 10 == 0 else None

    def solve_subproblem(self, subproblem, impact, charIndex, spIndex, carry):
        if charIndex == len(subproblem):
            new_carry = self.check_subproblem(subproblem, impact, carry)
            return self.backtracking_search(spIndex + 1, new_carry) if new_carry is not None else None

        char = subproblem[charIndex]

        if self.variables[char] is None:
            current_domain = self.domains[char].copy()
        
            common_domain = reduce(set.intersection, (set(c.satisfied(char)) for c in self.constraints))
            self.domains[char] = list(common_domain)

            for val in self.domains[char]:
                self.variables[char] = val
                assign = self.solve_subproblem(subproblem, impact, charIndex + 1, spIndex, carry)
                if assign is not None:
                    return assign
            
            self.variables[char] = None
            self.domains[char] = current_domain
        else:
            return self.solve_subproblem(subproblem, impact, charIndex + 1, spIndex, carry)

    def backtracking_search(self, index=0, carry=0):
        if len(self.variables) > 10:
            return None 

        if index == len(self.subproblems):
            return self.variables if carry == 0 else None

        return self.solve_subproblem(self.subproblems[index], self.impact[index], 0, index, carry)
    