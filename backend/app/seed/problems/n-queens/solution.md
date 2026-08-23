## 思路

- 按行放皇后：每一行恰好一个，冲突只可能来自「同一列」或「同一条对角线」。
- 用三个布尔数组分别标记列、主对角线 `row - col`、副对角线 `row + col` 是否已被占用；`row - col` 加上 `n - 1` 后下标非负。
- 第 `row` 行枚举列 `c`，未冲突则打标、递归下一行，回溯时清标。
- 搜到第 `n` 行说明 `n` 个皇后都放下了，方案数加一；本题只要计数，不必保存棋盘。
- `n ≤ 9`，搜索空间可接受；三个数组把「这一格能不能放」变成 O(1) 查询。

## 复杂度

- 时间：O(n!)（按行搜索，剪枝后仍与排列量级相当）
- 空间：O(n)（标记数组 + 递归栈）

## 模板代码

### Python3

```python
import sys


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    col = [False] * n
    diag1 = [False] * (2 * n)
    diag2 = [False] * (2 * n)
    ans = 0

    def dfs(row: int) -> None:
        nonlocal ans
        if row == n:
            ans += 1
            return
        for c in range(n):
            d1 = row - c + n - 1
            d2 = row + c
            if col[c] or diag1[d1] or diag2[d2]:
                continue
            col[c] = diag1[d1] = diag2[d2] = True
            dfs(row + 1)
            col[c] = diag1[d1] = diag2[d2] = False

    dfs(0)
    print(ans)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, ans;
vector<int> col, diag1, diag2;

void dfs(int row) {
    if (row == n) {
        ++ans;
        return;
    }
    for (int c = 0; c < n; ++c) {
        int d1 = row - c + n - 1;
        int d2 = row + c;
        if (col[c] || diag1[d1] || diag2[d2]) continue;
        col[c] = diag1[d1] = diag2[d2] = 1;
        dfs(row + 1);
        col[c] = diag1[d1] = diag2[d2] = 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    col.assign(n, 0);
    diag1.assign(2 * n, 0);
    diag2.assign(2 * n, 0);
    dfs(0);
    cout << ans << '\n';
    return 0;
}
```
