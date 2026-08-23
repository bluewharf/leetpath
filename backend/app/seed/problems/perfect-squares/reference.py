import math
import sys


def is_square(x: int) -> bool:
    r = math.isqrt(x)
    return r * r == x


def num_squares(n: int) -> int:
    if is_square(n):
        return 1
    x = n
    while x % 4 == 0:
        x //= 4
    if x % 8 == 7:
        return 4
    i = 1
    while i * i <= n:
        if is_square(n - i * i):
            return 2
        i += 1
    return 3


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    print(num_squares(n))


if __name__ == "__main__":
    main()
