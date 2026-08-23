import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    mat = []
    idx = 2
    for _ in range(n):
        mat.append(data[idx : idx + n])
        idx += n
    for i in range(n):
        for j in range(i + 1, n):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    for i in range(n):
        mat[i].reverse()
    print(n, n)
    for row in mat:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
