import sys
from collections import defaultdict


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    k = int(data[n + 1])
    cnt: dict[int, int] = defaultdict(int)
    cnt[0] = 1
    s = 0
    ans = 0
    for x in nums:
        s += x
        ans += cnt[s - k]
        cnt[s] += 1
    print(ans)


if __name__ == "__main__":
    main()
