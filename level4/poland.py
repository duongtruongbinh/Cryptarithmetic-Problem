import re

def is_operator(char):
    return char in "+-*"

# Ref: https://www.tutorialspoint.com/data_structures_algorithms/expression_parsing.htm
def infix_to_prefix(expression):
    precedence = {"+": 1, "-": 1, "*": 2}
    output = []
    operator_stack = []

    for char in expression:
        if isinstance(char, str) and char.isalnum():
            output.append(char)
        elif is_operator(char):
            while (operator_stack and
                   is_operator(operator_stack[-1]) and
                   precedence[char] <= precedence[operator_stack[-1]]):
                output.append(operator_stack.pop())
            operator_stack.append(char)
        elif char == "(":
            operator_stack.append(char)
        elif char == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remove "(" from the stack

    while operator_stack:
        output.append(operator_stack.pop())

    return output

def tokenize_expression(expression):
    left_side, _ = expression.split('=')
    # Sử dụng regular expression để tách chuỗi thành các thành phần (chữ cái và phép toán)
    tokens = re.findall(r'[A-Z]+|[-+=*()]', left_side)

    # Xóa khoảng trắng nếu có
    tokens = [token.strip() for token in tokens]

    return tokens

# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.left = None
#         self.right = None


# def build_prefix_tree(prefix_expression):
#     stack = []

#     for char in prefix_expression:
#         if isinstance(char, str) and char.isalnum():
#             node = Node(char)
#             stack.append(node)
#         elif char in "+-*/":
#             node = Node(char)
#             node.right = stack.pop()
#             node.left = stack.pop()
#             stack.append(node)

#     return stack[0]  # The final tree will be at the top of the stack

def evaluate(expression):
  # splitting expression at whitespaces
  #expression = expression.split()
   
  # stack
  stack = []
   
  # iterating expression
  for ele in expression:
     
    # ele is a number
    if ele not in '/*+-':
      stack.append(int(ele))
     
    # ele is an operator
    else:
      # getting operands
      right = stack.pop()
      left = stack.pop()
       
      # performing operation according to operator
      if ele == '+':
        stack.append(left + right)
         
      elif ele == '-':
        stack.append(left - right)
         
      elif ele == '*':
        stack.append(left * right)
         
      elif ele == '/':
        stack.append(int(left / right))
   
  # return final answer.
  return stack.pop()


# def postorder_traversal_to_list(node, prefix_expression):
#     if node:
#         postorder_traversal_to_list(node.left, prefix_expression)
#         postorder_traversal_to_list(node.right, prefix_expression)
#         prefix_expression.append(node.value)








