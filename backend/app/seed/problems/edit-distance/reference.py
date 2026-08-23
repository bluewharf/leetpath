import sys


def main() -> None:
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    lines = data.split("\n")
    w1 = lines[0] if lines else ""
    w2 = lines[1] if len(lines) > 1 else ""
    n, m = len(w1), len(w2)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        cur[0] = i
        a = w1[i - 1]
        for j in range(1, m + 1):
            if a == w2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    print(prev[m])


if __name__ == "__main__":
    main()
