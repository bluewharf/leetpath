## 思路

- 行首大于上一行行尾，整张表在行优先下就是一段严格的有序序列。
- 对下标区间 `[0, m·n−1]` 做二分，`mid` 映射到 `(mid / n, mid % n)`。
- 之后与普通有序数组二分完全相同：等于即命中，小了往右、大了往左。
- 不必先按行二分再按列二分，一次对数查找即可。

## 复杂度

- 时间：O(log(mn))
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    matrix: list[list[int]] = []
    idx = 2
    for _ in range(m):
        matrix.append(data[idx : idx + n])
        idx += n
    target = data[idx]
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            print("true")
            return
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print("false")


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
    vector<vector<int>> matrix(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> matrix[i][j];
    int target;
    cin >> target;
    int lo = 0, hi = m * n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int val = matrix[mid / n][mid % n];
        if (val == target) {
            cout << "true\n";
            return 0;
        }
        if (val < target) lo = mid + 1;
        else hi = mid - 1;
    }
    cout << "false\n";
    return 0;
}
```
