## 思路

### 解法一（推荐）：压成一维二分

- 行首大于上一行行尾，整张表在行优先下就是一段严格的有序序列。
- 对下标区间 `[0, m·n−1]` 做二分，`mid` 映射到 `(mid / n, mid % n)`。
- 之后与普通有序数组二分完全相同：等于即命中，小了往右、大了往左。
- 不必先按行二分再按列二分，一次对数查找即可。

### 解法二：先二分行再二分列

- 用每行最后一个元素定位 target 可能在哪一行，再在该行二分。
- 两次独立二分，O(log m + log n) = O(log(mn))，与解法一同阶。
- 行定位时注意边界：小于第一行首或大于最后一行尾直接不存在。

### 解法三：从右上角排除

- 与「搜索二维矩阵 II」同一招：大于 target 左移，小于则下移。
- 没用上「行尾 < 下一行首」的更强有序性，时间掉到 O(m+n)。
- 能做对，但不是这题该用的最优形状。

## 复杂度

- 解法一：时间 O(log(mn))，空间 O(1)
- 解法二：时间 O(log m + log n)，空间 O(1)
- 解法三：时间 O(m + n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
    # 行尾 < 下一行首，整表行优先即一段有序序列；空表时 hi=-1，循环不进
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]  # 一维下标映射回 (行, 列)
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
    // 行尾 < 下一行首，整表行优先即一段有序序列；空表时 hi=-1
    int lo = 0, hi = m * n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int val = matrix[mid / n][mid % n];  // 一维下标映射回 (行, 列)
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
