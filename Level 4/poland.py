def is_operator(char):
    return char in "+-*"

def infix_to_prefix(expression):
    operator_precedence = {"+": 1, "-": 1, "*": 2}
    prefix_expression = []
    operator_stack = []

    for char in expression:
        if char.isalnum():
            prefix_expression.append(char)
        elif is_operator(char):
            while operator_stack and is_operator(operator_stack[-1]) and operator_precedence[char] <= operator_precedence[operator_stack[-1]]:
                prefix_expression.append(operator_stack.pop())
            operator_stack.append(char)
        elif char == "(":
            operator_stack.append(char)
        elif char == ")":
            while operator_stack and operator_stack[-1] != "(":
                prefix_expression.append(operator_stack.pop())
            operator_stack.pop()  # Remove "(" from the stack

    while operator_stack:
        prefix_expression.append(operator_stack.pop())

    return prefix_expression

def evaluate_prefix(expression):
    stack = []
   
    for ele in expression:
        if ele not in '/*+-':
            stack.append(int(ele))
        else:
            right = stack.pop()
            left = stack.pop()
            if ele == '+':
                stack.append(left + right)
            elif ele == '-':
                stack.append(left - right)
            elif ele == '*':
                stack.append(left * right)
            elif ele == '/':
                stack.append(int(left / right))
   
    return stack.pop()
