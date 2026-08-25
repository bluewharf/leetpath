## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：滚动斐波那契（推荐）
- 到第 `n` 阶只能从 `n-1` 跨 1 阶，或从 `n-2` 跨 2 阶，所以 `f(n) = f(n-1) + f(n-2)`。
- `f(1)=1`、`f(2)=2`，后面就是斐波那契递推；最后一步不同，不会重复计数。
- 只要滚动保存前两项，不必整表。模板即此写法。
- 本题 `n <= 45`，`int` 足够，O(n) 扫一遍就过。

### 解法二：DP 数组
- `dp[i] = dp[i-1] + dp[i-2]`，`dp[1]=1`，`dp[2]=2`，答案 `dp[n]`。
- 与解法一转移完全相同，只是把历史留在数组里，方便打印过程或改成「每次 1/2/3 阶」。
- 时间 O(n)，空间 O(n)；能写但对这题是多余的。

### 解法三：矩阵快速幂
- 把递推写成 `[[f(n)], [f(n-1)]] = [[1,1],[1,0]]^(n-2) * [[f(2)],[f(1)]]`（或等价形式）。
- 矩阵幂用分治，`O(log n)` 次 2×2 乘法，适合 n 到 10^18 的后续题。
- 本题 n 很小，矩阵是加分项，不是第一选择。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(log n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    n = int(sys.stdin.read().strip())
    if n <= 2:
        print(n)
        return
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)


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
    if (n <= 2) {
        cout << n << '\n';
        return 0;
    }
    int a = 1, b = 2;
    for (int i = 3; i <= n; ++i) {
        int c = a + b;
        a = b;
        b = c;
    }
    cout << b << '\n';
    return 0;
}
```
