import re

def normalize_equation(equation: str) -> str:
    normalized = []
    inside_parentheses = False
    for char in equation:
        if char.isalpha():
            normalized.append(char)
        elif char == '(':
            inside_parentheses = normalized and normalized[-1] == '-'      
        elif char == ')':
            inside_parentheses = False
        elif inside_parentheses:
            normalized.append('-' if char == '+' else '+')
        else:
            normalized.append(char)

    return ''.join(normalized)

def parse_input(equation):
        variables = {variable: None for variable in equation if variable.isalpha()}
        domains = {var: [i for i in range(10)] for var in variables}
        words = re.findall(r'[A-Z]+', equation)
        operands, result  = words[:-1], words[-1]
        operators = ['+']

        for i in range(len(equation)):
            if equation[i] == '+':
                if equation[i+1] == '-':
                    operators.append('-')
                elif equation[i+1].isalpha() and equation[i-1].isalpha():
                    operators.append('+')
            elif equation[i] == '-':
                if equation[i+1] == '-':
                    operators.append('+')
                elif equation[i+1].isalpha() and equation[i-1].isalpha():
                    operators.append('-')
                    
        return [variables, domains, operators, operands, result]

def create_subproblem(operands, operators, result):
    # Calculate the maximum number of subproblems based on the length of the normalized and operands
    max_subprob_length = max(len(result), max(len(operand) for operand in operands))
    
    # Initialize subproblems and impact with empty lists and dictionaries
    subproblems = [[] for _ in range(max_subprob_length)]
    impact = [{} for _ in range(max_subprob_length)]
    
    # Calculate impact and construct subproblems for each operand
    for operand, operator in zip(operands, operators):
        for i, letter in enumerate(operand):
            offset = max_subprob_length - len(operand) + i
            if letter not in impact[offset]:
                subproblems[offset].append(letter)
                impact[offset][letter] = 0
            impact[offset][letter] += -1 if operator == '-' else 1

    # Calculate impact and construct subproblems for the result
    for i, letter in enumerate(result):
        offset = max_subprob_length - len(result) + i
        if letter not in impact[offset]:
            subproblems[offset].append(letter)
            impact[offset][letter] = 0
        impact[offset][letter] += -1

    # Reverse subproblems and impact to follow the original order
    subproblems.reverse()
    impact.reverse()

    return subproblems, impact

def read_file(filepath: str) -> str:
        with open(filepath, 'r') as file:
            equation = file.readline()
        return equation

def write_file(filepath, solution) -> None:
    with open(filepath, 'w') as file:
        if solution:
            vars = sorted(solution.keys())
            for var in vars:
                file.write(str(solution[var]))
        else:
            file.write("NO SOLUTION")