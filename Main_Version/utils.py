import re, sys

def get_command_line_arguments() -> list:
    return sys.argv

def tokenize_expression(expression):
    # Sử dụng regular expression để tách chuỗi thành các thành phần (chữ cái và phép toán)
    tokens = re.findall(r'[A-Z]+|[-+=*()]', expression)

    # Xóa khoảng trắng nếu có
    tokens = [token.strip() for token in tokens]

    return tokens

def parse_input(equation):
        variables = {variable: None for variable in equation if variable.isalpha()}
        domains = {var: [i for i in range(10)] for var in variables}
        words = re.findall(r'[A-Z]+', equation)
        operands, result = words[:-1], words[-1]
        expression, _  = equation.split('=')
        expression = tokenize_expression(expression)
        return [variables, domains, operands, expression, result]

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
            