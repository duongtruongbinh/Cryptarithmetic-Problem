import problem


# equation = 'SEND+MORE=MONEY'
# equation = 'SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+MOON+AS+HE+HAS+AT+THE+OTHER+TEN=TESTS'


for level in range(1, 2):
    for i in range(1, 4):
        crytharithmetic = problem.CryptarithmeticProblem(
            f'Level {level}/input_{i}.txt')
        print(crytharithmetic.operators)
        solution = crytharithmetic.solve()
        crytharithmetic.write_file(f'Level {level}/output_{i}.txt', solution)
        if solution:
            vars = sorted(solution.keys())
            for var in vars:
                print(var, end='')
            print('=', end='')
            for var in vars:
                print(solution[var], end='')
            print()
        else:
            print("NO SOLUTION")
