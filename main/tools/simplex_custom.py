import numpy as np
import math

# c = [1, 1, 0, 0, 0]
# A = [
#     [-1, 1, 1, 0, 0],
#     [1, 0, 0, 1, 0],
#     [0, 1, 0, 0, 1]
# ]
# b = [2, 4, 4]


def to_tableau(c, A, b):
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return xb + [z]


def can_be_improved(tableau):
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])


def get_pivot_position(tableau):
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)

    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    if (all([r == math.inf for r in restrictions])):
        raise Exception("Linear program is unbounded.")

    row = restrictions.index(min(restrictions))
    return row, column


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier

    return new_tableau


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions


def simplex(c, A, b):
    tableau = to_tableau(c, A, b)

    while can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    return get_solution(tableau)


# c = [7200, -50400, 0, 0, 0, 0]
# A = [
#     [1028.6, 0,     1,  0, 0,  0],
#     [0,      50400, 0, -1, 0,  0],
#     [1,      0,     0, 0, -1,  0],
#     [0,      1,     0, 0,  0, -1]
# ]
# b = [4.8, 5.625, 0, 0]


if __name__ == '__main__':
    c = [7200, -50400]
    A = [
        [1028.6, 0],
        [0,      -50400],
        [-1,      0],
        [0,      -1]
    ]
    b = [4.8, -5.625, 0, 0]

    solution = simplex(c, A, b)
    print('solution: ', solution)
    print(f"F = {sum([n1 * n2 for n1, n2 in zip(c, solution)])}")

    ps = lambda kk, a, c, p: kk * c * p / a
    pt = lambda kn, a, c, p: kn * a * c * p

    print(f"{ps(solution[0], 7, 90, 80)}")
    print(f"{pt(solution[1], 7, 90, 80)}")
