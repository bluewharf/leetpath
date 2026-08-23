import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    jumps = 0
    cur_end = 0
    far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = far
    print(jumps)


if __name__ == "__main__":
    main()
