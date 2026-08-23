import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    h = list(map(int, data[1 : 1 + n]))
    if n == 0:
        print(0)
        return
    l, r = 0, n - 1
    left_max, right_max = 0, 0
    ans = 0
    while l <= r:
        if h[l] <= h[r]:
            if h[l] >= left_max:
                left_max = h[l]
            else:
                ans += left_max - h[l]
            l += 1
        else:
            if h[r] >= right_max:
                right_max = h[r]
            else:
                ans += right_max - h[r]
            r -= 1
    print(ans)


if __name__ == "__main__":
    main()
