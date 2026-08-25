## 思路

### 解法一（推荐）：DFS + 原地标记

- 从每个格子当起点 DFS：当前格必须等于 `word[k]`，再向四连通走 `k+1`。
- 同一格不能复用：走进去时改成哨兵，回溯时还原，相当于路径上的 visited。
- `k` 走到 `word` 长度即成功；越界或字母对不上立刻剪枝。
- 词比网格还长时直接 false；否则最坏指数级，但 m、n ≤ 6、|word| ≤ 15，可接受。
- 找到任意一条路径即可返回，不必搜完全部起点。

### 解法二：DFS + 显式 visited

- 同样四连通回溯，但用 `vis[m][n]`（或下标集合）标记路径上的格子，离开时清掉。
- 不变量与解法一相同，不改原棋盘，适合棋盘是不可变/共享的场合。
- 与解法一差在多 O(mn) 标记数组；递归深度仍是 O(L)。

### 解法三：频次剪枝后再 DFS

- 先统计棋盘与单词的字母个数，单词某字母比棋盘多则直接 false；必要时把单词反转（从更稀有的一端搜）。
- 真正搜索仍走解法一的回溯，只是减少无效起点和死胡同。
- 最坏复杂度不变，数据有大量重复字母时剪枝很明显。

## 复杂度

- 解法一：时间 O(mn · 4^L)，空间 O(L)（递归深度；原地标记不额外开 vis），L 为单词长度
- 解法二：时间 O(mn · 4^L)，空间 O(mn + L)
- 解法三：时间 O(mn · 4^L)（剪枝后实践更快），空间 O(L) 或 O(字符集)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def exist(board, word):
    m, n = len(board), len(board[0])
    wlen = len(word)
    if wlen > m * n:
        return False  # 词比格子还多，不可能不重复走完

    def dfs(i, j, k):
        if k == wlen:
            return True
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        tmp = board[i][j]
        board[i][j] = "#"  # 原地哨兵：路径上不可复用
        found = (
            dfs(i + 1, j, k + 1)
            or dfs(i - 1, j, k + 1)
            or dfs(i, j + 1, k + 1)
            or dfs(i, j - 1, k + 1)
        )
        board[i][j] = tmp  # 回溯还原，别的起点还能用这格
        return found

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True  # 找到一条即可
    return False


def main() -> None:
    # 读入：m n、字符矩阵、单词
    data = sys.stdin.read().split()
    m, n = int(data[0]), int(data[1])
    idx = 2
    board = []
    for _ in range(m):
        board.append(list(data[idx : idx + n]))
        idx += n
    word = data[idx]
    print("true" if exist(board, word) else "false")


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
    // 读入：m n、字符矩阵、单词
    int m, n;
    cin >> m >> n;
    vector<vector<char>> board(m, vector<char>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cin >> board[i][j];
    string word;
    cin >> word;
    int wlen = (int)word.size();
    if (wlen > m * n) {
        cout << "false\n";
        return 0;
    }
    function<bool(int, int, int)> dfs = [&](int i, int j, int k) -> bool {
        if (k == wlen) return true;
        if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] != word[k]) return false;
        char tmp = board[i][j];
        board[i][j] = '#';  // 路径占用
        bool found = dfs(i + 1, j, k + 1) || dfs(i - 1, j, k + 1) ||
                     dfs(i, j + 1, k + 1) || dfs(i, j - 1, k + 1);
        board[i][j] = tmp;  // 回溯还原
        return found;
    };
    bool ok = false;
    for (int i = 0; i < m && !ok; i++) {
        for (int j = 0; j < n && !ok; j++) {
            if (board[i][j] == word[0] && dfs(i, j, 0)) ok = true;
        }
    }
    cout << (ok ? "true" : "false") << "\n";
    return 0;
}
```
