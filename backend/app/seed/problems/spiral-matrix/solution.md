## 思路

- 用四个边界 `top/bottom/left/right` 圈出当前层，按右→下→左→上走完一圈再向内收缩。
- 走完上边后 `top++`，走完右边后 `right--`，保证下一步不会重复访问拐角。
- 向左、向上前要再判断 `top <= bottom`、`left <= right`，否则单行/单列会把已遍历的格子再扫一遍。
- 每走完一条边就收缩对应边界，循环条件是矩形尚未退化成空。
- 总步数等于格子数，每个元素恰好入答案一次。

## 复杂度

- 时间：O(mn)
- 空间：O(1)（不计答案数组）

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
    ans = []
    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            ans.append(mat[top][j])
        top += 1
        for i in range(top, bottom + 1):
            ans.append(mat[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                ans.append(mat[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                ans.append(mat[i][left])
            left += 1
    print(" ".join(map(str, ans)))


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
    vector<int> ans;
    int top = 0, bottom = m - 1, left = 0, right = n - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) ans.push_back(mat[top][j]);
        top++;
        for (int i = top; i <= bottom; i++) ans.push_back(mat[i][right]);
        right--;
        if (top <= bottom) {
            for (int j = right; j >= left; j--) ans.push_back(mat[bottom][j]);
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; i--) ans.push_back(mat[i][left]);
            left++;
        }
    }
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```
