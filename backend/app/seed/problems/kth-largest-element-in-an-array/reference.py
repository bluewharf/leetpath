import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    print(sorted(nums, reverse=True)[k - 1])


if __name__ == "__main__":
    main()
