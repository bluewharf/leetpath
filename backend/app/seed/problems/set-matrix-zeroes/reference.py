import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    first_row = any(mat[0][j] == 0 for j in range(n))
    first_col = any(mat[i][0] == 0 for i in range(m))
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    if first_row:
        for j in range(n):
            mat[0][j] = 0
    if first_col:
        for i in range(m):
            mat[i][0] = 0
    print(m, n)
    for row in mat:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
