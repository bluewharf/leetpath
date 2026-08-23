import sys


def main() -> None:
    n = int(sys.stdin.read().strip())
    if n <= 2:
        print(n)
        return
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)


if __name__ == "__main__":
    main()
