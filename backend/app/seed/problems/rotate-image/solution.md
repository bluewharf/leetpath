## 思路

- 顺时针 90° 可以拆成两步原地操作：先转置，再把每一行左右翻转。
- 转置只枚举上三角 `j > i`，把 `(i, j)` 与 `(j, i)` 互换，避免换两次回到原地。
- 行翻转之后，原第 i 行变成新矩阵的第 n−1−i 列，正好是顺时针 90°。
- 不另开矩阵：两次都在原数组上完成。

## 复杂度

- 时间：O(n²)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    mat: list[list[int]] = []
    idx = 2
    for _ in range(n):
        mat.append(data[idx : idx + n])
        idx += n
    for i in range(n):
        for j in range(i + 1, n):
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
    cin >> m >> n;
    vector<vector<int>> mat(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> mat[i][j];
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
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
