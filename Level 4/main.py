from cryptarithmetic_problem import CryptarithmeticProblem

if __name__ == "__main__":
    equation = 'MXA*XVL=XXMSWK'
    # equation = 'SEND+(MORE+MONEY)-OR+DIE=NUOYI'
    # equation = "SEND+MORE=MONEY"
    problem = CryptarithmeticProblem(equation)
    print(problem.prefix_expression)
    solution = problem.solve_cryptarithmetic({})

    if solution:
        vars = sorted(solution.keys())
        for var in vars:
            print(f'{var}: {solution[var]}', end=' | ')
        print('\n')
        for operand in problem.operands:
            print(operand, end='=')
            operand_value = ''.join(str(solution[c]) for c in operand)
            print(operand_value, end='\n')
            
        print(problem.result, end=' = ')
        result = ''.join(str(solution[c]) for c in problem.result)
        print(result, end='\n\n')

    else:
        print("NO SOLUTION")