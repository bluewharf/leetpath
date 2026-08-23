## 思路

- 到第 `n` 阶只能从 `n-1` 跨 1 阶，或从 `n-2` 跨 2 阶，所以 `f(n) = f(n-1) + f(n-2)`。
- `f(1)=1`、`f(2)=2`，后面就是斐波那契递推。
- 两种走法的最后一步不同，不会重复计数。
- 只要滚动保存前两项，不必整表。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

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
