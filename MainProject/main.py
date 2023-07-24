from cryptarithmetic_problem import CryptarithmeticProblem
from utils import write_file

if __name__ == "__main__":

    #     equation = "MO-M=S"
    #     problem = CryptarithmeticProblem(equation)
    #     solution = problem.backtracking_search()

    #     if solution:
    #         for word in problem.operands:
    #             print(''.join(str(solution[c]) for c in word))
    #         print(''.join(str(solution[c]) for c in problem.result))
    #         vars = sorted(solution.keys())
    #         for var in vars:
    #             print(f'{var}: {solution[var]}')
    #     else:
    #         print("No solution found")

    for level in range(1, 4):
        for i in range(1, 6):
            problem = CryptarithmeticProblem(
                f'Level {level}/input_{i}.txt')
            print(problem.equation)
            solution = problem.backtracking_search()
            write_file(
                f'Level {level}/output_{i}.txt', solution)

            if solution:
                vars = sorted(solution.keys())
                for var in vars:
                    print(f'{var}: {solution[var]}', end=' | ')
                print('\n')
                sum = 0
                for operand, operator in zip(problem.operands, problem.operators):
                    print(operand, end='=')
                    operand_value = ''.join(str(solution[c]) for c in operand)
                    print(operand_value, end='\n')
                    if operator == '+':
                        sum = sum + int(operand_value)
                    else:
                        sum = sum - int(operand_value)
                print("Sum = ", sum)
                print(problem.result, end=' = ')
                result = ''.join(str(solution[c]) for c in problem.result)
                print(result, end='\n\n')
                print(sum == int(result))

            else:
                print("NO SOLUTION")
