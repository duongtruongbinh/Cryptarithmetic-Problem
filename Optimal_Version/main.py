from cryptarithmetic_problem import CryptarithmeticProblem
from utils import *
import time

if __name__ == "__main__":
    file_path = str(get_command_line_arguments()[1])
    folder, file = file_path.split('/')
    name, tail = file.split('.')
    _, index = name.split('_')
    equation = read_file(f'{file_path}')

    problem = CryptarithmeticProblem(equation)
    print(f'{file_path}')
    print(equation)

    start_time = time.time()
    solution = problem.backtracking_search()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")

    write_file(
        f'{folder}/output_{index}.txt', solution)
    if solution:
        vars = sorted(solution.keys())
        for var in vars:
            print(f'{var}: {solution[var]}', end=' | ')
        print('\n')
    else:
        print("NO SOLUTION\n")
