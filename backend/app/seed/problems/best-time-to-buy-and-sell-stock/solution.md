## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：一次遍历维护历史最低价（推荐）
- 只允许一买一卖，卖出日 `i` 的最优买入就是 `i` 之前的历史最低价，利润 `prices[i] - minSoFar`。
- 从左扫到右，边走边维护「目前见过的最低价」和「目前最大利润」，每个候选卖出日都被考虑到。
- 某天利润为负说明今天不该卖，最大利润保持原值；全程没有正利润就输出 0。
- 不需要枚举所有买卖对：历史最低价单调更新，信息足够。模板即此写法。

### 解法二：动态规划（持有 / 不持有）
- `hold` 表示当前持有股票的最大收益（买了所以是负数或扣掉买入价），`sold` 表示已卖出的最大收益。
- 转移：`hold = max(hold, -price)`，`sold = max(sold, hold + price)`，因为只能交易一次。
- 与解法一本质相同，只是把「最低买入价」改写成状态机，方便推广到冷冻期、手续费、最多 k 笔。
- 时间 O(n)、空间 O(1)；面试若追问「多次买卖」就从这套状态往外加。

### 解法三：枚举买卖对
- 枚举卖出日 `j`，再在 `[0, j)` 里找最小买入价，或直接双重循环算 `prices[j]-prices[i]`。
- 正确但时间 O(n²)。本题 `n` 到 `10^5`，必超时，只适合口头对比或数据极小的验算。
- 由此能看出解法一把内层「找历史最低」摊成了一次扫描。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n²)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    prices = data[1 : 1 + n]
    min_price = prices[0]
    best = 0
    for p in prices[1:]:
        if p - min_price > best:
            best = p - min_price
        if p < min_price:
            min_price = p
    print(best)


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
    vector<int> prices(n);
    for (int i = 0; i < n; ++i) cin >> prices[i];
    int min_price = prices[0];
    int best = 0;
    for (int i = 1; i < n; ++i) {
        best = max(best, prices[i] - min_price);
        min_price = min(min_price, prices[i]);
    }
    cout << best << '\n';
    return 0;
}
```
