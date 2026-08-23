import math
import sys


def main() -> None:
    m, n = map(int, sys.stdin.read().split())
    print(math.comb(m + n - 2, m - 1))


if __name__ == "__main__":
    main()
