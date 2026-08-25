## 思路

### 解法一（推荐）：一维滚动 DP

- 到达 `(i, j)` 的方案 = 从上方来 + 从左方来；第一行、第一列只有一种走法。
- 滚动成一维：`dp[j] += dp[j-1]`，`dp[j]` 旧值是上一行，`dp[j-1]` 是本行左边，空间压到 O(n)。
- 初始 `dp` 全 1，对应第一行；从第二行开始更新列 `1..n-1`。
- `m=1` 或 `n=1` 时内层不更新，答案保持 1，边界自然对。
- 与二维 DP 同一转移，只是把上一行复用在同一个数组里。

### 解法二：二维 DP

- `dp[i][j] = dp[i-1][j] + dp[i][j-1]`，第一行第一列置 1。
- 不变量一眼能看：每个格子的方案来自上方和左方，没有别的入口。
- 与解法一差在多开一张表，方便讲清转移；空间 O(mn)，可以同样滚成一行。

### 解法三：组合数

- 一共要走 `(m-1)` 次下和 `(n-1)` 次右，路径条数是 `C(m+n-2, m-1)`（或 `C(m+n-2, n-1)`）。
- 用乘法累乘 / 除法约分算组合数，注意中间溢出，用 64 位整数。
- 时间降到 O(min(m, n))，不再填表；和 DP 在「无障碍网格」上等价，有障碍时组合数失效、必须改回 DP。

## 复杂度

- 解法一：时间 O(mn)，空间 O(n)
- 解法二：时间 O(mn)，空间 O(mn)
- 解法三：时间 O(min(m, n))，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    m, n = map(int, sys.stdin.read().split())
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    print(dp[-1])


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
    vector<long long> dp(n, 1);
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] += dp[j - 1];
        }
    }
    cout << dp[n - 1] << "\n";
    return 0;
}
```
