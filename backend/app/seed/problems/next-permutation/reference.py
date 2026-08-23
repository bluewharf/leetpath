import sys


def next_permutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1 :] = reversed(nums[i + 1 :])


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    next_permutation(nums)
    print(*nums)


if __name__ == "__main__":
    main()
