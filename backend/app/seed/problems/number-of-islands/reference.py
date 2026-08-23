import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(data[idx : idx + n])
        idx += n
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] != 1:
                continue
            ans += 1
            stack = [(i, j)]
            grid[i][j] = 0
            while stack:
                x, y = stack.pop()
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 0
                        stack.append((nx, ny))
    print(ans)


if __name__ == "__main__":
    main()
