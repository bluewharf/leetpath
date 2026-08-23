import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    intervals = []
    idx = 2
    for _ in range(m):
        intervals.append((data[idx], data[idx + 1]))
        idx += n
    intervals.sort()
    merged: list[list[int]] = []
    for a, b in intervals:
        if not merged or merged[-1][1] < a:
            merged.append([a, b])
        else:
            if b > merged[-1][1]:
                merged[-1][1] = b
    for a, b in merged:
        print(a, b)


if __name__ == "__main__":
    main()
