import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    idx = 2
    a = []
    for _ in range(m):
        a.append(data[idx : idx + n])
        idx += n
    m2, n2 = data[idx], data[idx + 1]
    idx += 2
    b = []
    for _ in range(m2):
        b.append(data[idx : idx + n2])
        idx += n2
    min_r = min_c = 10**9
    max_r = max_c = -1
    for i in range(m):
        for j in range(n):
            if a[i][j] != b[i][j]:
                min_r = min(min_r, i)
                max_r = max(max_r, i)
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    if max_r < 0:
        print(-1)
    else:
        print(min_r, min_c, max_r, max_c)


if __name__ == "__main__":
    main()
