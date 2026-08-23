## 思路

- 拉格朗日四平方定理：任何自然数都能写成至多 4 个完全平方数之和，所以答案只可能是 1、2、3、4。
- 本身是平方 → 1；先除掉因子 4，若剩下的数 `≡ 7 (mod 8)`，则必须是 4（勒让德三平方定理）。
- 再枚举 `i²`，若 `n - i²` 也是平方 → 2。
- 其余情况只能是 3。O(√n) 判定，不必做完全背包。

## 复杂度

- 时间：O(√n)
- 空间：O(1)

## 模板代码

### Python3

```python
import math
import sys


def is_square(x: int) -> bool:
    r = math.isqrt(x)
    return r * r == x


def num_squares(n: int) -> int:
    if is_square(n):
        return 1
    x = n
    while x % 4 == 0:
        x //= 4
    if x % 8 == 7:
        return 4
    i = 1
    while i * i <= n:
        if is_square(n - i * i):
            return 2
        i += 1
    return 3


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
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r * r == x;
}

int numSquares(int n) {
    if (isSquare(n)) return 1;
    int x = n;
    while (x % 4 == 0) x /= 4;
    if (x % 8 == 7) return 4;
    for (int i = 1; i * i <= n; ++i) {
        if (isSquare(n - i * i)) return 2;
    }
    return 3;
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
