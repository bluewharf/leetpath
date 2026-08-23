import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    grid: list[list[int]] = []
    idx = 2
    for _ in range(m):
        grid.append(data[idx : idx + n])
        idx += n

    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    print(dp[m - 1][n - 1])


if __name__ == "__main__":
    main()
