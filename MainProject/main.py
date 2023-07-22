from cryptarithmetic_problem import CryptarithmeticProblem

if __name__ == "__main__":
    equation = "SEND+(MORE+MONEY)-OR+DIE=NUOYI"
    problem = CryptarithmeticProblem(equation)
    solution = problem.backtracking_search()
    for word in problem.operands:
        print(''.join(str(solution[c]) for c in word))
    print(''.join(str(solution[c]) for c in problem.result))
    if solution:
        vars = sorted(solution.keys())
        for var in vars:
            print(f'{var}: {solution[var]}')
    else:
        print("No solution found")