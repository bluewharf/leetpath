import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        print("true")
        return
    m, n = data[0], data[1]
    iv = []
    idx = 2
    for _ in range(m):
        iv.append((data[idx], data[idx + 1]))
        idx += n
    iv.sort()
    ok = True
    for i in range(1, len(iv)):
        if iv[i][0] < iv[i - 1][1]:
            ok = False
            break
    print("true" if ok else "false")


if __name__ == "__main__":
    main()
