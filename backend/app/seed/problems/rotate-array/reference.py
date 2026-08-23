import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    if n == 0:
        print()
        return
    k %= n
    if k:
        nums = nums[-k:] + nums[:-k]
    print(" ".join(map(str, nums)))


if __name__ == "__main__":
    main()
