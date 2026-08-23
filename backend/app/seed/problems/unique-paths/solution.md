## 思路

- 只能向右或向下，从左上到右下一共要走 `(m-1)` 次下和 `(n-1)` 次右，路径条数就是组合数 `C(m+n-2, m-1)`。
- DP 视角：到达 `(i, j)` 的方案 = 从上方来 + 从左方来，第一行/第一列只有一种走法。
- 滚动成一维：`dp[j] += dp[j-1]`，`dp[j]` 旧值是上一行，`dp[j-1]` 是本行左边，空间压到 O(n)。
- `m=1` 或 `n=1` 时内层不更新，答案保持 1，边界自然对。

## 复杂度

- 时间：O(m n)
- 空间：O(n)

## 模板代码

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
