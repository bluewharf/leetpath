## 思路

### 解法一：二维 DP（推荐）

- 只能向右或向下，到达 `(i, j)` 的路径必来自正上或正左，取两者较小再加格子本身。
- `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`；第一行/第一列没有选择，只能沿边界累加。
- 子问题无后效：格子非负，局部最小拼起来就是全局最小，不必搜索。
- 起点 `dp[0][0] = grid[0][0]`，答案在右下角。
- 整张表留下最好默写，和滚动数组/原地修改转移完全相同。

### 解法二：滚动数组

- 每行只依赖上一行和本行左侧，用一维 `dp[j]` 表示当前行。
- `dp[j]` 先加上方（旧值就是上一行），再与 `dp[j-1]` 取 min；第一列只加上方。
- 转移与解法一相同，空间压到 O(n)；模板留二维表更直观。

### 解法三：原地改 grid

- 直接在 `grid` 上累加最小路径，省掉 `dp` 数组。
- 读入后不再使用原格子，语义允许；若题目禁止破坏输入则必须另开表。
- 和二维 DP 差在「结果写回输入」，边界处理仍是先填第一行/列。

## 复杂度

- 解法一：时间 O(mn)，空间 O(mn)
- 解法二：时间 O(mn)，空间 O(n)
- 解法三：时间 O(mn)，空间 O(1)（不计输入网格）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：二维 DP。第一行/列只能沿边界累加，其余取上/左较小者再加格子。
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(data[idx : idx + n])
        idx += n
    # dp[i][j]：走到 (i,j) 的最小路径和。只能向右/向下，无后效。
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]  # 第一行只能从左来
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]  # 第一列只能从上来
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    print(dp[m - 1][n - 1])


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：二维 DP。第一行/列只能沿边界累加，其余取上/左较小者再加格子。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cin >> grid[i][j];
    vector<vector<int>> dp(m, vector<int>(n));
    dp[0][0] = grid[0][0];
    for (int j = 1; j < n; j++) dp[0][j] = dp[0][j - 1] + grid[0][j];  // 第一行只能从左
    for (int i = 1; i < m; i++) dp[i][0] = dp[i - 1][0] + grid[i][0];  // 第一列只能从上
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    cout << dp[m - 1][n - 1] << '\n';
    return 0;
}
```
