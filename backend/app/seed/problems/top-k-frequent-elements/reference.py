import sys
from collections import Counter


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    k = int(data[n + 1])
    cnt = Counter(nums)
    ranked = sorted(cnt.keys(), key=lambda x: (-cnt[x], x))
    print(" ".join(str(x) for x in ranked[:k]))


if __name__ == "__main__":
    main()
