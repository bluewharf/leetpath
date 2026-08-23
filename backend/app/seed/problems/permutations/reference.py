import itertools
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    perms = sorted(itertools.permutations(nums))
    for p in perms:
        print(*p)


if __name__ == "__main__":
    main()
