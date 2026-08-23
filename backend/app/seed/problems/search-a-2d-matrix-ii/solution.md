## 思路

- 行与行之间可能交错，不能把整表压成一段有序数组再二分。
- 从左下角出发：当前值是该行最小、该列最大，一次比较就能丢掉一行或一列。
- 大于 target 则整行都更大，上移；小于 target 则整列都更小，右移。
- 走到越界仍未命中就是不存在。从右上角出发对称，思路一样。

## 复杂度

- 时间：O(m + n)
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
