from cryptarithmetic_problem import CryptarithmeticProblem
from utils import *

if __name__ == "__main__":
    for level in range(1, 5):
        for i in range(1, 6):
            problem = CryptarithmeticProblem(f'Level {level}\input_{i}.txt')
            print(f'Level {level}\input_{i}.txt')
            print(problem.equation)
            solution = problem.solve_cryptarithmetic({})
            write_file(f'Level {level}/output_{i}.txt', solution)
            if solution:
                vars = sorted(solution.keys())
                for var in vars:
                    print(f'{var}: {solution[var]}', end=' | ')
                print('\n')
            else:
                print("NO SOLUTION\n")