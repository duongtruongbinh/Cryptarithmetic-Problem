from cryptarithmetic_problem import CryptarithmeticProblem

if __name__ == "__main__":
    equation = "SEND+(MORE+MONEY)-OR+DIE=NUOYI"
    problem = CryptarithmeticProblem(equation)
    solution = problem.backtracking_search()
    if solution:
        vars = sorted(solution.keys())
        for var in vars:
            print(var, end='')
        print('=', end='')
        for var in vars:
            print(solution[var], end='')
        print()
    else:
        print("No solution found")