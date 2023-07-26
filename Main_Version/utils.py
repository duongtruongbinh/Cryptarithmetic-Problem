import re, sys

def get_command_line_arguments() -> list:
    return sys.argv

def normalize_equation(equation: str) -> str:
    normalized = []
    inside_parentheses = False
    inside_multiplication = False
    mul_operand = []
    
    for i, char in enumerate(equation):
        # Handling alphanumeric characters
        if char.isalpha():
            normalized.append(char)
        elif char == '(':
            if normalized:
                # Check if inside parentheses and/or multiplication
                inside_parentheses = normalized and normalized[-1] == '-' 
                inside_multiplication = normalized and normalized[-1] == '*' 
                if inside_multiplication:
                    index = None
                    # Copy the elements before the previous non-alphanumeric character
                    for idx in range(len(normalized) - 2, -1, -1):
                        if normalized[idx] in '+-*':
                            index = idx
                            break
                    mul_operand = normalized[index : -1]
        elif char == ')':
            inside_parentheses, inside_multiplication = False, False
        elif inside_parentheses:
            # Handle signs inside parentheses
            if char == '*':
                normalized.append('*')
            else:
                normalized.append('-' if char == '+' else '+')
        elif inside_multiplication:
            # Handle signs inside multiplication
            temp = mul_operand.copy()
            if char == '-':
                temp[0] = '-' if mul_operand[0] == '+' else '+'
                if equation[i-1] == '(':
                    normalized= normalized[:index]  
            normalized.extend(temp)
            normalized.append('*')
        else:
            # Handle signs outside parentheses or multiplication
            if equation[i] == '+':
                if equation[i+1] == '-':
                    normalized.append('-')
                elif equation[i+1].isalpha() and equation[i-1] not in '+-*':
                    normalized.append('+')
            elif equation[i] == '-':
                if equation[i+1] == '-':
                    normalized.append('+')
                elif equation[i+1].isalpha() and equation[i-1] not in '+-*':
                    normalized.append('-')
            elif equation[i] == '*':
                index = None
                for idx in range(len(normalized) - 1, -1, -1):
                    if normalized[idx] in '+-*':
                        index = idx
                        break
                if equation[i+1] == '-':
                    normalized[index] = '-' if normalized[index] == '+' else  '+'
                normalized.append('*')                
    return ''.join(normalized)

def tokenize_expression(expression):
    # Sử dụng regular expression để tách chuỗi thành các thành phần (chữ cái và phép toán)
    tokens = re.findall(r'[A-Z]+|[-+=*()]', expression)

    # Xóa khoảng trắng nếu có
    tokens = [token.strip() for token in tokens]

    return tokens

def parse_input(equation):
        variables = set(variable for variable in equation if variable.isalpha())
        domains = {var: [i for i in range(10)] for var in variables}
        words = re.findall(r'[A-Z]+', equation)
        operands, result = words[:-1], words[-1]
        expression, t_result  = equation.split('=')
        expression = tokenize_expression(normalize_equation(expression))
        operator_result = '+' if t_result[0].isalpha() else '-'
        return [variables, domains, operands, expression, (operator_result, result)]

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
            