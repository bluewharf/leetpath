import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    cand = 0
    cnt = 0
    for v in nums:
        if cnt == 0:
            cand = v
        cnt += 1 if v == cand else -1
    print(cand)


if __name__ == "__main__":
    main()
