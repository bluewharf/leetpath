## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：完全背包一维 DP（推荐）
- `dp[x]` 表示凑出金额 `x` 的最少枚数，`dp[0]=0`，其余先标成「不可能」（哨兵 `amount+1`）。
- 转移 `dp[x] = min(dp[x], dp[x-coin] + 1)`，金额对硬币正序枚举，同一面额可以反复用。
- 面额大于 `amount` 的硬币直接跳过；结束时仍是哨兵则输出 `-1`。
- 模板即此写法，空间压成一维。

### 解法二：BFS 按枚数分层
- 把金额看成图上的点，用一枚硬币走一步；最短路的边数就是最少枚数。
- 队列里是「当前金额」，访问过的金额不再入队，第一次到达 `amount` 就是答案。
- 时间最坏仍 O(n · amount)，但「最少步数」语义更直观；凑不出则 BFS 结束返回 `-1`。
- 当面额很大、可达金额很稀疏时，可能比填满整张 DP 表更早结束。

### 解法三：记忆化 DFS
- `dfs(remain)` 返回凑出 `remain` 的最少枚数，枚举下一枚硬币并缓存。
- 不记忆化会指数爆炸；记忆化后与 DP 同阶，但递归深度和常数通常更差。
- 适合先讲搜索再改成解法一；落地仍用循环 DP。

## 复杂度

- 解法一：时间 O(n · amount)，空间 O(amount)
- 解法二：时间 O(n · amount)，空间 O(amount)
- 解法三：时间 O(n · amount)，空间 O(amount)（缓存 + 递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    coins = list(map(int, data[1 : 1 + n]))
    amount = int(data[1 + n])
    inf = amount + 1
    dp = [inf] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        if coin > amount:
            continue
        for x in range(coin, amount + 1):
            cand = dp[x - coin] + 1
            if cand < dp[x]:
                dp[x] = cand
    print(-1 if dp[amount] >= inf else dp[amount])


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
    int n;
    cin >> n;
    vector<int> coins(n);
    for (int i = 0; i < n; ++i) cin >> coins[i];
    int amount;
    cin >> amount;
    int inf = amount + 1;
    vector<int> dp(amount + 1, inf);
    dp[0] = 0;
    for (int coin : coins) {
        if (coin > amount) continue;
        for (int x = coin; x <= amount; ++x) {
            dp[x] = min(dp[x], dp[x - coin] + 1);
        }
    }
    cout << (dp[amount] >= inf ? -1 : dp[amount]) << '\n';
    return 0;
}
```
