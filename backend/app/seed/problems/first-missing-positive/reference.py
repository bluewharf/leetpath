import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0]) if data else 0
    nums = list(map(int, data[1 : 1 + n]))
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            print(i + 1)
            return
    print(n + 1)


if __name__ == "__main__":
    main()
