import re

def normalize_equation(equation: str) -> str:
    equation = equation.upper()
    normalized = []
    inside_parentheses = False
    inside_multiplication = False
    mul_operand = []
    for char in equation:
        if char.isalpha():
            normalized.append(char)
        elif char == '(':
            inside_parentheses = normalized and normalized[-1] == '-'
            inside_multiplication = normalized and normalized[-1] == '*'
            if inside_multiplication:
                temp = []
                for i in range(len(normalized) - 2, -1, -1):
                    temp.append(normalized[i])
                    if not normalized[i].isalpha():
                        break
                mul_operand = temp.copy()
                mul_operand.reverse()
        elif char == ')':
            inside_parentheses, inside_multiplication = False, False
        elif inside_parentheses:
            if char == '*':
                normalized.append('*')
            else:
                normalized.append('-' if char == '+' else '+')
        elif inside_multiplication:
            if mul_operand[0] == '+':
                if char == '-':
                    mul_operand[0] = '-' 
            else:
                if char == '-':
                    mul_operand[0] = '+' 
            normalized.extend(mul_operand)
            normalized.append('*')
        else:
            normalized.append(char)

    return ''.join(normalized)

def split_equation(equation: str) -> list:
    variables = {variable: None for variable in equation if variable.isalpha()}
    words = re.findall(r'[A-Z]+', equation)
    operands, result = words[:-1], words[-1]
    operators = re.findall(r'[+\-*]', equation)
    operators[:0] = ['+']
    domains = {var: [i for i in range(10)] for var in variables}
    return variables, domains, operators, operands, result

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
