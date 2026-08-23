import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : n + 1]))
    target = int(data[n + 1])
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in seen:
            print(seen[y], i)
            return
        seen[x] = i


if __name__ == "__main__":
    main()
