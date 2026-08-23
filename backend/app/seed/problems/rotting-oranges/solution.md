## 思路

- 多源 BFS：所有初始腐烂橘子同时入队，当作第 0 分钟的感染源。
- 每分钟把四邻的新鲜橘子变烂并入队，用入队时的时间戳记录层数。
- 先统计新鲜数；扩散结束还有新鲜橘子则不可能全部腐烂，答案为 −1。
- 一开始就没有新鲜橘子，答案是 0。

## 复杂度

- 时间：O(mn)
- 空间：O(mn)

## 模板代码

### Python3

```python
import sys
from collections import deque


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    grid: list[list[int]] = []
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
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> grid[i][j];

    queue<array<int, 3>> q;
    int fresh = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 2) q.push({i, j, 0});
            else if (grid[i][j] == 1) fresh++;
        }
    }
    if (fresh == 0) {
        cout << 0 << '\n';
        return 0;
    }

    int minutes = 0;
    const int dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (!q.empty()) {
        auto [i, j, t] = q.front();
        q.pop();
        minutes = t;
        for (auto& d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && grid[ni][nj] == 1) {
                grid[ni][nj] = 2;
                fresh--;
                q.push({ni, nj, t + 1});
            }
        }
    }
    cout << (fresh ? -1 : minutes) << '\n';
    return 0;
}
```
