## 思路

- 扫一遍网格：每碰到一块还没访问的陆地，岛屿数加一，并把这块四连通陆地整片淹掉。
- 只有上下左右算同一座岛，斜对角不相通。
- 用栈做迭代 DFS（或 BFS），访问时原地把 `1` 改成 `0`，省掉 vis，也避免递归在细长岛屿上爆栈。
- 每个格子最多进栈一次，总工作量与网格规模成线性。

## 复杂度

- 时间：O(mn)
- 空间：O(mn)（最坏整图是陆地时的栈）

## 模板代码

### Python3

```python
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
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j) cin >> grid[i][j];
    const int dx[4] = {1, -1, 0, 0};
    const int dy[4] = {0, 0, 1, -1};
    int ans = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] != 1) continue;
            ++ans;
            stack<pair<int, int>> st;
            st.push({i, j});
            grid[i][j] = 0;
            while (!st.empty()) {
                auto [x, y] = st.top();
                st.pop();
                for (int k = 0; k < 4; ++k) {
                    int nx = x + dx[k], ny = y + dy[k];
                    if (nx >= 0 && nx < m && ny >= 0 && ny < n && grid[nx][ny] == 1) {
                        grid[nx][ny] = 0;
                        st.push({nx, ny});
                    }
                }
            }
        }
    }
    cout << ans << '\n';
    return 0;
}
```
