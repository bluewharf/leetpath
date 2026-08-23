## 思路

- 完全背包：`dp[x]` 表示凑出金额 `x` 的最少枚数，`dp[0]=0`，其余先标成「不可能」。
- 转移 `dp[x] = min(dp[x], dp[x - coin] + 1)`，金额对硬币正序枚举，同一面额可以反复用。
- 面额大于 `amount` 的硬币直接跳过，避免无意义下标。
- 结束时 `dp[amount]` 仍是哨兵值，说明凑不出，输出 -1。

## 复杂度

- 时间：O(n · amount)
- 空间：O(amount)

## 模板代码

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
