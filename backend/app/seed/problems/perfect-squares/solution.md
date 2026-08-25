## 思路

### 解法一（推荐）：四平方定理判定

- 拉格朗日四平方定理：任何自然数都能写成至多 4 个完全平方数之和，所以答案只可能是 1、2、3、4。
- 本身是平方 → 1；先除掉因子 4，若剩下的数 `≡ 7 (mod 8)`，则必须是 4（勒让德三平方定理）。
- 再枚举 `i²`，若 `n - i²` 也是平方 → 2。
- 其余情况只能是 3。O(√n) 判定，不必做完全背包。

### 解法二：完全背包

- `dp[s]` 为凑出 `s` 所需最少平方数个数，转移枚举 `j² ≤ s`：`dp[s] = min(dp[s], dp[s - j²] + 1)`。
- 不依赖数论，和「零钱兑换」同一模板。
- `n` 到 10⁴ 时 O(n√n) 可过；更大就要看时限，通常不如定理判定。

### 解法三：BFS 最短路

- 从 `n` 出发，每次减去一个平方数，第一次到达 0 的层数就是答案。
- 完全背包的图论视角：边权全 1，最短路 = 最少个数。
- 答案 ≤ 4，搜索很浅；需要 `vis` 避免重复入队。

## 复杂度

- 解法一：时间 O(√n)，空间 O(1)
- 解法二：时间 O(n√n)，空间 O(n)
- 解法三：时间 O(n√n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import math
import sys


def is_square(x: int) -> bool:
    r = math.isqrt(x)
    return r * r == x


def num_squares(n: int) -> int:
    # 四平方定理：答案只可能是 1/2/3/4，按判定顺序排除
    if is_square(n):
        return 1
    x = n
    while x % 4 == 0:
        x //= 4
    if x % 8 == 7:  # 勒让德：n=4^k(8m+7) 必须四个平方数
        return 4
    i = 1
    while i * i <= n:
        if is_square(n - i * i):  # 拆成两个平方
            return 2
        i += 1
    return 3  # 其余只能是 3


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    print(num_squares(n))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isSquare(int x) {
    long long r = (long long)sqrt((double)x);
    while (r * r > x) --r;  // 纠正浮点 sqrt 可能的偏差
    while ((r + 1) * (r + 1) <= x) ++r;
    return r * r == x;
}

int numSquares(int n) {
    // 四平方定理：答案只可能是 1/2/3/4
    if (isSquare(n)) return 1;
    int x = n;
    while (x % 4 == 0) x /= 4;
    if (x % 8 == 7) return 4;  // 勒让德：n=4^k(8m+7) 必须四个平方数
    for (int i = 1; i * i <= n; ++i) {
        if (isSquare(n - i * i)) return 2;  // 拆成两个平方
    }
    return 3;  // 其余只能是 3
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << numSquares(n) << '\n';
    return 0;
}
```
