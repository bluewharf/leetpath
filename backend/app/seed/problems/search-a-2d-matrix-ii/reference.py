import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    matrix = []
    idx = 2
    for _ in range(m):
        matrix.append(data[idx : idx + n])
        idx += n
    target = data[idx]
    i, j = m - 1, 0
    while i >= 0 and j < n:
        val = matrix[i][j]
        if val == target:
            print("true")
            return
        if val > target:
            i -= 1
        else:
            j += 1
    print("false")


if __name__ == "__main__":
    main()
