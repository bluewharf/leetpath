import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            print("false")
            return
        far = max(far, i + x)
    print("true")


if __name__ == "__main__":
    main()
