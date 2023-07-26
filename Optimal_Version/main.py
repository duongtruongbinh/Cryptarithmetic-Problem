from cryptarithmetic_problem import CryptarithmeticProblem
from utils import read_file, write_file
import time

if __name__ == "__main__":
    for level in range(1, 4):
        for i in range(1, 6):
            equation = read_file(f'Cryptarithmetic-Problem\Level {level}\input_{i}.txt')
            problem = CryptarithmeticProblem(equation)
            print(f'Cryptarithmetic-Problem\Level {level}\input_{i}.txt')
            print(equation)
            
            start_time = time.time()
            solution = problem.backtracking_search()
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution Time:", execution_time, "seconds")
            
            write_file(
                f'Cryptarithmetic-Problem\Level {level}/output_{i}.txt', solution)
            if solution:
                vars = sorted(solution.keys())
                for var in vars:
                    print(f'{var}: {solution[var]}', end=' | ')
                print('\n')
            else:
                print("NO SOLUTION\n")
