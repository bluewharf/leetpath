import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    imax = imin = ans = nums[0]
    for x in nums[1:]:
        candidates = (x, imax * x, imin * x)
        imax = max(candidates)
        imin = min(candidates)
        if imax > ans:
            ans = imax
    print(ans)


if __name__ == "__main__":
    main()
