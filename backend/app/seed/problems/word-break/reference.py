import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    m = int(sys.stdin.readline())
    words = set()
    for _ in range(m):
        words.add(sys.stdin.readline().rstrip("\n"))
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    print("true" if dp[n] else "false")


if __name__ == "__main__":
    main()
