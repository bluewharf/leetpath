import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    h = list(map(int, data[1 : 1 + n]))
    l, r = 0, n - 1
    best = 0
    while l < r:
        hl, hr = h[l], h[r]
        if hl < hr:
            best = max(best, hl * (r - l))
            l += 1
        else:
            best = max(best, hr * (r - l))
            r -= 1
    print(best)


if __name__ == "__main__":
    main()
