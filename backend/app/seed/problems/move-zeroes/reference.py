import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    write = 0
    for x in nums:
        if x != 0:
            nums[write] = x
            write += 1
    for i in range(write, n):
        nums[i] = 0
    if n:
        print(" ".join(map(str, nums)))
    else:
        print()


if __name__ == "__main__":
    main()
