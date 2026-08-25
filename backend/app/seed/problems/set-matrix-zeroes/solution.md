## 思路

### 解法一（推荐）：首行首列原地标记

- 用第 0 行、第 0 列充当「这一列/这一行需要置零」的布尔数组，额外空间 O(1)。
- 先单独记下第 0 行、第 0 列本身是否本来就有 0，避免标记和真实零互相污染。
- 扫描子矩阵 `(1..m, 1..n)`：遇到 0 就把 `matrix[i][0]` 和 `matrix[0][j]` 写成 0。
- 再扫一遍子矩阵，行头或列头为 0 则把该格置零；最后才根据预先记录清掉第 0 行/第 0 列。
- 必须后清边界：否则边界上的标记会被提前抹掉，内部置零会漏。

### 解法二：行标记数组 + 列标记数组

- 开 `row[m]`、`col[n]`，第一遍遇到 0 就记 `row[i]=col[j]=true`。
- 第二遍若该行或该列被标记，则把格子写成 0。
- 不变量更直观：标记与原矩阵分离，不用担心第 0 行/列被污染。
- 与解法一差在用 O(m+n) 换掉「边界复用」的细节，面试可先写这个再压空间。

### 解法三：先收集零坐标再置零

- 扫一遍把所有值为 0 的 `(i, j)` 放进列表，再对每个坐标整行整列置零。
- 同一行/列可能被多次清，可用集合去重行号列号，本质退化成解法二。
- 正确但零很多时写入次数更多，只适合当暴力对照。

## 复杂度

- 解法一：时间 O(mn)，空间 O(1)
- 解法二：时间 O(mn)，空间 O(m+n)
- 解法三：时间 O(mn · max(m, n))（不去重时），空间 O(零的个数)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    # 读入：m n，随后 m 行各 n 个整数
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    # 第 0 行/列既是数据又当标记，必须先记下它们本身有没有 0
    first_row = any(mat[0][j] == 0 for j in range(n))
    first_col = any(mat[i][0] == 0 for i in range(m))
    # 子矩阵遇 0：用行头、列头打标，不立刻整行整列清，避免把标记冲掉
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    # 边界最后清：否则内部还没根据标记置零，标记就被抹掉
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
    // 读入：m n，随后 m×n 矩阵
    int m, n;
    cin >> m >> n;
    vector<vector<int>> mat(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cin >> mat[i][j];
    // 第 0 行/列复用为标记前，先记下它们自己是否本来就有 0
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
    // 边界最后清，避免标记被提前抹掉
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
