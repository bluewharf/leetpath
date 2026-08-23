import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    total = sum(nums)
    if total % 2 != 0:
        print("false")
        return
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):
            if dp[s - x]:
                dp[s] = True
        if dp[target]:
            print("true")
            return
    print("true" if dp[target] else "false")


if __name__ == "__main__":
    main()
