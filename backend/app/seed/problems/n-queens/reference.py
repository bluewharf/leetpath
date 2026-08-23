import sys


def main() -> None:
    n = int(sys.stdin.read().strip())
    col = [False] * n
    diag1 = [False] * (2 * n)
    diag2 = [False] * (2 * n)
    ans = 0

    def dfs(row: int) -> None:
        nonlocal ans
        if row == n:
            ans += 1
            return
        for c in range(n):
            d1 = row - c + n - 1
            d2 = row + c
            if col[c] or diag1[d1] or diag2[d2]:
                continue
            col[c] = diag1[d1] = diag2[d2] = True
            dfs(row + 1)
            col[c] = diag1[d1] = diag2[d2] = False

    dfs(0)
    print(ans)


if __name__ == "__main__":
    main()
