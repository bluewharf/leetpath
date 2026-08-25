## 思路

### 解法一（推荐）：四边界收缩

- 用四个边界 `top/bottom/left/right` 圈出当前层，按右→下→左→上走完一圈再向内收缩。
- 走完上边后 `top++`，走完右边后 `right--`，保证下一步不会重复访问拐角。
- 向左、向上前要再判断 `top <= bottom`、`left <= right`，否则单行/单列会把已遍历的格子再扫一遍。
- 每走完一条边就收缩对应边界，循环条件是矩形尚未退化成空。
- 总步数等于格子数，每个元素恰好入答案一次。

### 解法二：方向数组 + 访问标记

- 方向循环 `(0,1) → (1,0) → (0,-1) → (-1,0)`，撞到边界或已访问格子就右转。
- 用 `visited` 矩阵（或改原值当哨兵）标记走过的格，走满 `m*n` 步结束。
- 不变量是「当前方向能走就走，不能走就转向」，单行单列不用特判。
- 与解法一差在：用 visited 换掉四边界的收缩细节，空间多 O(mn)，转弯逻辑更统一。

### 解法三：按层模拟

- 第 `k` 层的上边是第 `k` 行 `[k .. n-1-k]`，其余三边类推，`k` 从 0 到 `min(m,n)//2 - 1`。
- 本质与解法一相同，只是把四边界写成层号的函数；单行/单列仍要避免走回头。
- 层数公式容易在奇偶行列时写错，一般不如显式维护四个变量清晰。

## 复杂度

- 解法一：时间 O(mn)，空间 O(1)（不计答案数组）
- 解法二：时间 O(mn)，空间 O(mn)（visited）
- 解法三：时间 O(mn)，空间 O(1)（不计答案数组）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    # 读入：m n 与矩阵
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    ans = []
    # 当前层矩形 [top,bottom] × [left,right]，走完一条边立刻收缩对应边界
    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            ans.append(mat[top][j])
        top += 1  # 上边走完，拐角已计入，避免右边重复
        for i in range(top, bottom + 1):
            ans.append(mat[i][right])
        right -= 1
        # 单行/单列时矩形已退化，不能再走回头
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
    // 读入：m n 与矩阵
    int m, n;
    cin >> m >> n;
    vector<vector<int>> mat(m, vector<int>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cin >> mat[i][j];
    vector<int> ans;
    // 四边界圈出当前层；走完一条边立刻收缩，拐角不重复
    int top = 0, bottom = m - 1, left = 0, right = n - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) ans.push_back(mat[top][j]);
        top++;
        for (int i = top; i <= bottom; i++) ans.push_back(mat[i][right]);
        right--;
        // 单行/单列已退化则不再走左、上，否则会回头
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
