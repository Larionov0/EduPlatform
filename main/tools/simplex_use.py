import numpy as np
# from simplex_custom import get_solution, simplex

# c = [-7200, 50400, 0, 0, 0, 0]
# A = [
#     [1028.6, 0,     1,  0, 0,  0],
#     [0,      50400, 0, -1, 0,  0],
#     [1,      0,     0, 0, -1,  0],
#     [0,      1,     0, 0,  0, -1]
# ]
# b = [4.8, 5.625, 0, 0]


ps = lambda kk, a, c, p: kk * c * p / a
pt = lambda kn, a, c, p: kn * a * c * p


def main_test():
    c = [-7200, 50400]
    A = [
        [1028.6, 0],
        [0,      -50400],
        [-1,      0],
        [0,      -1]
    ]
    b = [4.8, -5.625, 0, 0]

    from scipy.optimize import linprog
    res = linprog(c, A_ub=A, b_ub=b, method='simplex', options={"disp": True, "presolve": False})
    print(res)

    print(f"{ps(res.x[0], 7, 90, 80)}")
    print(f"{pt(res.x[1], 7, 90, 80)}")


def solve(c, A, b):
    from scipy.optimize import linprog
    res = linprog(c, A_ub=A, b_ub=b, method='simplex',
                  options={"disp": True, "presolve": False})

    # print(f"{ps(res.x[0], 7, 90, 80)}")
    # print(f"{pt(res.x[1], 7, 90, 80)}")
    return [ps(res.x[0], 7, 90, 80), pt(res.x[1], 7, 90, 80), res.fun]


if __name__ == '__main__':
    main_test()
