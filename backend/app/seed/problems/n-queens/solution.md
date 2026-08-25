## 思路

### 解法一（推荐）：按行回溯 + 列/对角线标记

- 考回溯剪枝：每一行恰好一个皇后，冲突只可能来自同一列或同一条对角线。
- 三个布尔数组分别标记列、主对角线 `row - col`、副对角线 `row + col`；`row - col` 加上 `n - 1` 后下标非负。
- 第 `row` 行枚举列 `c`，未冲突则打标、递归下一行，回溯时清标。
- 搜到第 `n` 行说明 `n` 个皇后都放下了，方案数加一；本题只要计数，不必保存棋盘。
- `n ≤ 9`，O(1) 判冲突后搜索量仍与排列同阶，可以接受。

### 解法二：位运算压缩占用

- 列和两条对角线各用一个整数 bitmask，第 `c` 位为 1 表示占用，与布尔数组同一不变量。
- 可放位置是 `~(col | diag1 | diag2)` 的低 `n` 位；每次取最低位 1 试放，回溯用异或撤销。
- 和解法一只差状态表示，常数更小，是 N 皇后的常见加速写法。
- 本题 `n` 很小，正确性等价，面试能口述转移即可。

### 解法三：列的全排列 + 对角线检查

- 「每行一个、每列一个」⇔ 列下标是 `0 .. n-1` 的一个排列，先生成排列再检查。
- 两点冲突当且仅当 `row - col` 或 `row + col` 相同；有一对非法则丢弃。
- 比按行剪枝更晚发现冲突，搜索量通常更大，用来理解「皇后问题就是带约束的排列」。

## 复杂度

- 解法一：时间 O(n!)，空间 O(n)（标记数组 + 递归栈）
- 解法二：时间 O(n!)，空间 O(n)（递归栈；占用是常数个整数）
- 解法三：时间 O(n · n!)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
