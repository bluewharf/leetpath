import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    x = 0
    for v in nums:
        x ^= v
    print(x)


if __name__ == "__main__":
    main()
