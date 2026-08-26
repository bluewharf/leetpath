## 思路

扫一遍记下差异点的最小/最大行和列。没有差异就 `-1`。

### 解法一（推荐）：一次扫描维护四端

- 遍历每个格子，值不同则更新 `min_r/max_r/min_c/max_c`。
- 从未更新过则输出 `-1`。
- 先问是否同尺寸、要不要旋转矩形：本题轴对齐。

### 解法二：先收集差异点再 min/max

- 多一次存储，没必要。

## 复杂度

- 解法一：时间 O(HW)，空间 O(1)
- 解法二：时间 O(HW)，空间 O(差异点数)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    idx = 2
    a = []
    for _ in range(m):
        a.append(data[idx : idx + n])
        idx += n
    m2, n2 = data[idx], data[idx + 1]
    idx += 2
    b = []
    for _ in range(m2):
        b.append(data[idx : idx + n2])
        idx += n2
    min_r = min_c = 10**9
    max_r = max_c = -1
    for i in range(m):
        for j in range(n):
            if a[i][j] != b[i][j]:
                min_r = min(min_r, i)
                max_r = max(max_r, i)
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    if max_r < 0:
        print(-1)
    else:
        print(min_r, min_c, max_r, max_c)


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
    vector<vector<int>> a(m, vector<int>(n));
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j) cin >> a[i][j];
    int m2, n2;
    cin >> m2 >> n2;
    vector<vector<int>> b(m2, vector<int>(n2));
    for (int i = 0; i < m2; ++i)
        for (int j = 0; j < n2; ++j) cin >> b[i][j];
    int min_r = 1e9, min_c = 1e9, max_r = -1, max_c = -1;
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            if (a[i][j] != b[i][j]) {
                min_r = min(min_r, i);
                max_r = max(max_r, i);
                min_c = min(min_c, j);
                max_c = max(max_c, j);
            }
    if (max_r < 0) cout << -1 << '\n';
    else cout << min_r << ' ' << min_c << ' ' << max_r << ' ' << max_c << '\n';
    return 0;
}
```
