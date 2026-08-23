import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur + x < x else cur + x
        if cur > best:
            best = cur
    print(best)


if __name__ == "__main__":
    main()
