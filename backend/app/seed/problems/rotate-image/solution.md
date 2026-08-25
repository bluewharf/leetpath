## 思路

### 解法一（推荐）：转置 + 行翻转

- 顺时针 90° 可以拆成两步原地操作：先转置，再把每一行左右翻转。
- 转置只枚举上三角 `j > i`，把 `(i, j)` 与 `(j, i)` 互换，避免换两次回到原地。
- 行翻转之后，原第 i 行变成新矩阵的第 n−1−i 列，正好是顺时针 90°。
- 不另开矩阵：两次都在原数组上完成。

### 解法二：四元组循环交换

- 按层从外到内，每个位置沿 `(i,j) → (j, n-1-i) → (n-1-i, n-1-j) → (n-1-j, i)` 转一圈四个值。
- 一次到位，不经过转置中间态；要写对四个坐标映射。
- 与解法一比：少一次完整遍历，但边界（层数、每层起点终点）更容易偏一。

### 解法三：先上下翻转再转置

- 上下翻转后再转置也是顺时针 90°，与解法一只是分解顺序不同。
- 先左右翻转再转置是逆时针，符号搞反就会错。
- 记口诀：顺时针 = 转置 + 水平翻转 = 垂直翻转 + 转置。

## 复杂度

- 解法一：时间 O(n²)，空间 O(1)
- 解法二：时间 O(n²)，空间 O(1)
- 解法三：时间 O(n²)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]  # 读入 m n（方阵），idx 从 2 起跳过第二维
    mat: list[list[int]] = []
    idx = 2
    for _ in range(n):
        mat.append(data[idx : idx + n])
        idx += n
    # 顺时针 90° = 转置 + 每行左右翻转
    for i in range(n):
        for j in range(i + 1, n):  # 只换上三角，避免换两次回到原地
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    for i in range(n):
        mat[i].reverse()
    print(n, n)
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
    cin >> m >> n;  // 方阵，m == n
    vector<vector<int>> mat(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> mat[i][j];
    // 顺时针 90° = 转置 + 每行左右翻转
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)  // 只换上三角，避免换两次回到原地
            swap(mat[i][j], mat[j][i]);
    for (int i = 0; i < n; i++)
        reverse(mat[i].begin(), mat[i].end());
    cout << n << ' ' << n << '\n';
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (j) cout << ' ';
            cout << mat[i][j];
        }
        cout << '\n';
    }
    return 0;
}
```
