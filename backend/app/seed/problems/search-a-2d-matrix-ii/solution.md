## 思路

### 解法一（推荐）：从左下角排除

- 行与行之间可能交错，不能把整表压成一段有序数组再二分。
- 从左下角出发：当前值是该行最小、该列最大，一次比较就能丢掉一行或一列。
- 大于 target 则整行都更大，上移；小于 target 则整列都更小，右移。
- 走到越界仍未命中就是不存在。从右上角出发对称，思路一样。

### 解法二：每行（或每列）二分

- 每一行各自有序，对 m 行各做一次二分。
- 时间 O(m log n)，行很少、列很多时可以；最坏不如排除法。
- 没有利用「列也递增」，所以比解法一弱。

### 解法三：分治丢象限

- 取中间列（或中心），在该列上二分找到分割点，至少一个象限可以整块丢掉，再递归其余象限。
- 正确性来自 Young 表的偏序：中心左上更小、右下更大。
- 实现重，常数也大，面试能讲「丢掉一块」即可，落地仍推解法一。

## 复杂度

- 解法一：时间 O(m + n)，空间 O(1)
- 解法二：时间 O(m log n)，空间 O(1)
- 解法三：时间约 O(n^{log₂ 3})（方阵常见分析），空间 O(log n)（递归）

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
    i, j = m - 1, 0
    while i >= 0 and j < n:
        val = matrix[i][j]
        if val == target:
            print("true")
            return
        if val > target:
            i -= 1
        else:
            j += 1
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
    int i = m - 1, j = 0;
    while (i >= 0 && j < n) {
        int val = matrix[i][j];
        if (val == target) {
            cout << "true\n";
            return 0;
        }
        if (val > target) i--;
        else j++;
    }
    cout << "false\n";
    return 0;
}
```
