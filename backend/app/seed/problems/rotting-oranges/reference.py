import sys
from collections import deque


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(data[idx : idx + n])
        idx += n

    q: deque[tuple[int, int, int]] = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                q.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1

    if fresh == 0:
        print(0)
        return

    minutes = 0
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while q:
        i, j, t = q.popleft()
        minutes = t
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                grid[ni][nj] = 2
                fresh -= 1
                q.append((ni, nj, t + 1))

    print(-1 if fresh else minutes)


if __name__ == "__main__":
    main()
