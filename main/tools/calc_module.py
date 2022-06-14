from main.tools.simplex_use import solve


def optimize_price(a, c, p, C_t_min, C_s_min, p_t_ser, p_s_ser):
    C = [-c * p, c * p * a]
    A = [
        [c * p / a, 0],
        [0, -c * p * a],
        [-1, 0],
        [0, -1]
    ]
    b = [p_s_ser/(C_s_min/100 + 1), -p_t_ser * (C_t_min/100 + 1), 0, 0]

    print(C)
    print(A),
    print(b)

    res = solve(C, A, b)  # ps, pt, price
    return [res[0], res[1], -res[2]]


if __name__ == '__main__':
    # print(optimize_price(7, 90, 80, -10, 4, 6.25, 5))
    print(optimize_price(7, 90, 80, -10, 4, 250, 200))
