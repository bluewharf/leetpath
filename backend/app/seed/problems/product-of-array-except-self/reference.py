import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    ans = [1] * n
    pref = 1
    for i in range(n):
        ans[i] = pref
        pref *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= suf
        suf *= nums[i]
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
