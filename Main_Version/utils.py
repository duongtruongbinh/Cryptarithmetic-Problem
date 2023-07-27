import re, sys

def get_command_line_arguments() -> list:
    return sys.argv

def normalized_expression(expression):
    normalized = []
    inside_multiplication = False
    change_operator = False
    i = 0
    while i != len(expression):
        # Handling alphanumeric characters
        if expression[i].isalpha():
            normalized.append(expression[i])
        elif expression[i] == '(':
            if expression[i-1] == '*':
                inside_multiplication = True
            normalized.append(expression[i])
        elif expression[i] == ')':
            inside_multiplication, change_operator = False, False
            normalized.append(expression[i])
        elif inside_multiplication:
            if expression[i] == '-':
                if expression[i-1] == '(':
                    fe_idx, se_idx = 0, 0
                    close_parentheses_idx = expression.find(')', i)
                    for idx in range(i+1, close_parentheses_idx + 1): 
                        if expression[idx] in '+-)':
                            fe_idx = idx
                            break
                    f_operand = expression[i:fe_idx]
                    
                    plus_idx = expression.find('+', i, close_parentheses_idx)
                    if plus_idx == -1:
                        index = None
                        # Copy the elements before the previous non-alphanumeric character
                        for idx in range(len(normalized) - 1, -1, -1):
                            if normalized[idx] in '+-':
                                index = idx
                                break
                        normalized[index] = '-' if normalized[index] == '+' else '+'
                        change_operator = True
                    else:
                        for idx in range(plus_idx + 1, close_parentheses_idx + 1):
                            if expression[idx] in '+-)':
                                se_idx = idx
                                break
                        s_operand = expression[plus_idx+1:se_idx]
                        temp = s_operand + expression[fe_idx:plus_idx] + f_operand + expression[se_idx:close_parentheses_idx]
                        expression = expression[:i] + temp + expression[close_parentheses_idx:]
                        print(expression)
                        continue
                elif change_operator:
                    normalized.append('+')
                else:
                    normalized.append(expression[i])
            elif expression[i] == '+':
                if change_operator:
                    normalized.append('-')
                else:
                    normalized.append(expression[i])
        else:
            if expression[i] == '+':
                if expression[i+1] == '-':
                    normalized.append('-')
                elif (expression[i+1].isalpha() or expression[i+1] == '(' or expression[i+1] == '+') and expression[i-1] not in '+-*':
                    normalized.append('+')
            elif expression[i] == '-':
                if expression[i+1] == '-':
                    normalized.append('+')
                elif (expression[i+1].isalpha() or expression[i+1] == '(' or expression[i+1] == '+') and expression[i-1] not in '+-*':
                    normalized.append('-')
            elif expression[i] == '*':
                index = None
                for idx in range(len(normalized) - 1, -1, -1):
                    if normalized[idx] in '+-*':
                        index = idx
                        break
                if expression[i+1] == '-':
                    normalized[index] = '-' if normalized[index] == '+' else  '+'
                normalized.append('*')   
        i += 1             
            
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
        expression = tokenize_expression(normalized_expression(expression))
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
            