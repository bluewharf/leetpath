import math
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1 : 1 + n]
    m = data[1 + n]
    b = data[2 + n : 2 + n + m]
    dot = na = nb = 0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0 or nb == 0:
        print("0.0")
        return
    val = dot / (math.sqrt(na) * math.sqrt(nb))
    print(f"{val:.1f}")


if __name__ == "__main__":
    main()
