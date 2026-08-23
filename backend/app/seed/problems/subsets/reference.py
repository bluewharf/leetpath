import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    subsets: list[list[int]] = []
    for mask in range(1 << n):
        cur = [nums[i] for i in range(n) if mask & (1 << i)]
        cur.sort()
        subsets.append(cur)
    subsets.sort(key=lambda s: (len(s), s))
    for s in subsets:
        if s:
            print(*s)
        else:
            print()


if __name__ == "__main__":
    main()
