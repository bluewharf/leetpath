## 思路

- 只允许一买一卖，卖出日 `i` 的最优买入就是 `i` 之前的历史最低价，利润 `prices[i] - minSoFar`。
- 从左扫到右，边走边维护「目前见过的最低价」和「目前最大利润」，每个候选卖出日都被考虑到。
- 某天利润为负说明今天不该卖，最大利润保持原值；全程没有正利润就输出 0。
- 不需要枚举所有买卖对：历史最低价单调更新，信息足够。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

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
