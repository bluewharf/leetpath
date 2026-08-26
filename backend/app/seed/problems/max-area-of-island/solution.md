## 思路

和「岛屿数量」同一套淹岛，只是每次扩散时累加格子数，全局取 max。

### 解法一（推荐）：迭代 DFS 淹岛

- 扫到尚未访问的陆地，从这里 DFS/栈向四邻扩散，边走边把 `1` 改成 `0`，同时计数。
- 扩散结束得到这座岛的面积，更新全局最大。
- 全 0 时答案是 0；斜对角不算连通。
- 可以改原数组当 vis；面试先问能不能改图。

### 解法二：BFS

- 发现新陆地时改用队列扩散，计数方式相同。
- 细长岛屿不会递归爆栈，和 DFS 答案一致。

## 复杂度

- 解法一：时间 O(mn)，空间 O(mn)（最坏栈）
- 解法二：时间 O(mn)，空间 O(mn)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
            area = 0
            stack = [(i, j)]
            grid[i][j] = 0
            while stack:
                x, y = stack.pop()
                area += 1
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 0
                        stack.append((nx, ny))
            if area > ans:
                ans = area
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
    int dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    int ans = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] != 1) continue;
            int area = 0;
            vector<pair<int, int>> st;
            st.push_back({i, j});
            grid[i][j] = 0;
            while (!st.empty()) {
                auto [x, y] = st.back();
                st.pop_back();
                ++area;
                for (auto& d : dirs) {
                    int nx = x + d[0], ny = y + d[1];
                    if (nx >= 0 && nx < m && ny >= 0 && ny < n && grid[nx][ny] == 1) {
                        grid[nx][ny] = 0;
                        st.push_back({nx, ny});
                    }
                }
            }
            ans = max(ans, area);
        }
    }
    cout << ans << '\n';
    return 0;
}
```
