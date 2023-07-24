from cryptarithmetic_problem import CryptarithmeticProblem

if __name__ == "__main__":
    # equation = 'APD*AD=DPCED'
    equation = 'U*(SO-MI)=M'
    problem = CryptarithmeticProblem(equation)
    print(problem.prefix_expression)
    solution = problem.solve_cryptarithmetic({})

    if solution:
        print(solution)
        vars = sorted(solution.keys())
        for var in vars:
            print(solution[var], end='')
    else:
        print("No solution found.")
