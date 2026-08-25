## 思路

### 解法一（推荐）：多源 BFS + 时间戳

- 多源 BFS：所有初始腐烂橘子同时入队，当作第 0 分钟的感染源。
- 每分钟把四邻的新鲜橘子变烂并入队，用入队时的时间戳记录层数。
- 先统计新鲜数；扩散结束还有新鲜橘子则不可能全部腐烂，答案为 −1。
- 一开始就没有新鲜橘子，答案是 0。

### 解法二：分层 BFS（用队列大小）

- 不把时间塞进队列，每轮先记下当前队列长度，处理完一层再 `minutes++`。
- 与解法一等价，只是层数的记录方式不同：一层 = 一分钟。
- 最后一层出队后不要多加一分钟，否则全烂时会偏大。

### 解法三：按分钟扫描整图

- 每分钟扫一遍所有格子，把「将要腐烂」的先标记再统一改掉，模拟同时传播。
- 时间 O(mn · 答案)，答案最坏 O(mn)，比 BFS 慢一截。
- 漏掉「同时」会让同一分钟内新烂的橘子继续传，答案偏小。

## 复杂度

- 解法一：时间 O(mn)，空间 O(mn)
- 解法二：时间 O(mn)，空间 O(mn)
- 解法三：时间 O(m²n²)，空间 O(1) 额外（不计网格）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import deque


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]  # 读入网格：0 空、1 新鲜、2 腐烂
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
                q.append((i, j, 0))  # 多源 BFS：所有初始腐烂同时当第 0 分钟源
            elif grid[i][j] == 1:
                fresh += 1

    if fresh == 0:  # 边界：一开始就没有新鲜橘子
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
                grid[ni][nj] = 2  # 入队时标记腐烂，避免重复入队
                fresh -= 1
                q.append((ni, nj, t + 1))

    print(-1 if fresh else minutes)  # 扩散完仍有新鲜则不可能全部腐烂


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
    cin >> m >> n;  // 读入网格：0 空、1 新鲜、2 腐烂
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> grid[i][j];

    queue<array<int, 3>> q;
    int fresh = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 2) q.push({i, j, 0});  // 多源：初始腐烂同时当第 0 分钟源
            else if (grid[i][j] == 1) fresh++;
        }
    }
    if (fresh == 0) {  // 边界：一开始就没有新鲜橘子
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
                grid[ni][nj] = 2;  // 入队时标记，避免重复入队
                fresh--;
                q.push({ni, nj, t + 1});
            }
        }
    }
    cout << (fresh ? -1 : minutes) << '\n';  // 仍有新鲜则不可能全部腐烂
    return 0;
}
```
