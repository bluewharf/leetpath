## 思路

先写公式再写循环：点积除以两模长。不要先甩矩阵库。

### 解法一（推荐）：一遍累加点积和两个平方和

- `dot`、`na2`、`nb2` 同步累加。
- 分母为 0（零向量）返回 0。
- 输出按站点约定保留 1 位小数。

### 解法二：先算模再点积

- 两遍扫描，结果相同，代码稍散。

## 复杂度

- 解法一：时间 O(d)，空间 O(1)
- 解法二：时间 O(d)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import math
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1 : 1 + n]
    m = data[1 + n]
    b = data[2 + n : 2 + n + m]
    dot = na = nb = 0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0 or nb == 0:
        print("0.0")
        return
    val = dot / (math.sqrt(na) * math.sqrt(nb))
    print(f"{val:.1f}")


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
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    int m;
    cin >> m;
    vector<long long> b(m);
    for (int i = 0; i < m; ++i) cin >> b[i];
    long long dot = 0, na = 0, nb = 0;
    for (int i = 0; i < n; ++i) {
        dot += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }
    cout << fixed << setprecision(1);
    if (na == 0 || nb == 0) {
        cout << 0.0 << '\n';
        return 0;
    }
    double val = (double)dot / (sqrt((double)na) * sqrt((double)nb));
    cout << val << '\n';
    return 0;
}
```
