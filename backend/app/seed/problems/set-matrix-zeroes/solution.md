## 思路

- 原地标记：用第 0 行、第 0 列充当「这一列/这一行需要置零」的布尔数组，额外空间 O(1)。
- 先单独记下第 0 行、第 0 列本身是否本来就有 0，避免标记和真实零互相污染。
- 扫描子矩阵 `(1..m, 1..n)`：遇到 0 就把 `matrix[i][0]` 和 `matrix[0][j]` 写成 0。
- 再扫一遍子矩阵，行头或列头为 0 则把该格置零；最后才根据预先记录清掉第 0 行/第 0 列。
- 必须后清边界：否则边界上的标记会被提前抹掉，内部置零会漏。

## 复杂度

- 时间：O(mn)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    first_row = any(mat[0][j] == 0 for j in range(n))
    first_col = any(mat[i][0] == 0 for i in range(m))
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    if first_row:
        for j in range(n):
            mat[0][j] = 0
    if first_col:
        for i in range(m):
            mat[i][0] = 0
    print(m, n)
    for row in mat:
        print(" ".join(map(str, row)))


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
    vector<vector<int>> mat(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cin >> mat[i][j];
    bool first_row = false, first_col = false;
    for (int j = 0; j < n; j++)
        if (mat[0][j] == 0) first_row = true;
    for (int i = 0; i < m; i++)
        if (mat[i][0] == 0) first_col = true;
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            if (mat[i][j] == 0) {
                mat[i][0] = 0;
                mat[0][j] = 0;
            }
        }
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            if (mat[i][0] == 0 || mat[0][j] == 0) mat[i][j] = 0;
        }
    }
    if (first_row)
        for (int j = 0; j < n; j++) mat[0][j] = 0;
    if (first_col)
        for (int i = 0; i < m; i++) mat[i][0] = 0;
    cout << m << ' ' << n << '\n';
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (j) cout << ' ';
            cout << mat[i][j];
        }
        cout << '\n';
    }
    return 0;
}
```
