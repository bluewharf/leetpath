import sys

def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1:1+n]
    target = data[1+n]
    L = lower_bound(nums, target)
    if L == n or nums[L] != target:
        print(-1, -1)
        return
    R = lower_bound(nums, target + 1) - 1
    print(L, R)

if __name__ == "__main__":
    main()
