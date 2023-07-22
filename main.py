import problem


# test deparenthesize

problem = problem.CryptarithmeticProblem('Cryptarithmetic-Problem/Level 1/input_4.txt')

print(problem.words)
print(problem.operators)
print(problem.variables)
solution = problem.solve()
print(solution)
sorted_vars = sorted(solution.keys())
for word in problem.words:
    for char in word:
        print(solution[char], end='')
    print(' ', end='')
# for level in range(1, 2):
#     for i in range(1, 4):
#         crytharithmetic = problem.CryptarithmeticProblem(
#             f'Level {level}/input_{i}.txt')
#         print(crytharithmetic.operators)
#         solution = crytharithmetic.solve()
#         crytharithmetic.write_file(f'Level {level}/output_{i}.txt', solution)
#         if solution:
#             vars = sorted(solution.keys())
#             for var in vars:
#                 print(var, end='')
#             print('=', end='')
#             for var in vars:
#                 print(solution[var], end='')
#             print()
#         else:
#             print("NO SOLUTION")
