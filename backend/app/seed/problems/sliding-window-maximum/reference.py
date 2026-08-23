import sys
from collections import deque


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    dq: deque[int] = deque()
    ans: list[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            ans.append(nums[dq[0]])
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
