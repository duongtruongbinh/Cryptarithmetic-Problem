def is_operator(char):
    return char in "+-*"

def infix_to_postfix(expression):
    operator_precedence = {"+": 1, "-": 1, "*": 2}
    postfix_expression = []
    operator_stack = []

    for char in expression:
        if char.isalnum():
            postfix_expression.append(char)
        elif is_operator(char):
            while operator_stack and is_operator(operator_stack[-1]) and operator_precedence[char] <= operator_precedence[operator_stack[-1]]:
                postfix_expression.append(operator_stack.pop())
            operator_stack.append(char)
        elif char == "(":
            operator_stack.append(char)
        elif char == ")":
            while operator_stack and operator_stack[-1] != "(":
                postfix_expression.append(operator_stack.pop())
            operator_stack.pop()  # Remove "(" from the stack

    while operator_stack:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression

def evaluate_postfix(expression):
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
