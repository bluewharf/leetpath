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
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            print("true")
            return
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print("false")


if __name__ == "__main__":
    main()
