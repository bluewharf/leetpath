import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        print(0)
        return
    m, n = data[0], data[1]
    events = []
    idx = 2
    for _ in range(m):
        s, e = data[idx], data[idx + 1]
        events.append((s, 1))
        events.append((e, -1))
        idx += n
    events.sort(key=lambda x: (x[0], x[1]))  # 同一时刻先结束
    cur = ans = 0
    for _, d in events:
        cur += d
        if cur > ans:
            ans = cur
    print(ans)


if __name__ == "__main__":
    main()
