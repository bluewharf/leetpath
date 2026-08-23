## 思路

- 从每个格子当起点 DFS：当前格必须等于 `word[k]`，再向四连通走 `k+1`。
- 同一格不能复用：走进去时改成哨兵，回溯时还原，相当于路径上的 visited。
- `k` 走到 `word` 长度即成功；越界或字母对不上立刻剪枝。
- 词比网格还长时直接 false；否则最坏指数级，但 m、n ≤ 6、|word| ≤ 15，可接受。
- 找到任意一条路径即可返回，不必搜完全部起点。

## 复杂度

- 时间：O(m n · 4^L)，L 为单词长度
- 空间：O(L)（递归深度；原地标记不额外开 vis）

## 模板代码

### Python3

```python
import sys


def exist(board, word):
    m, n = len(board), len(board[0])
    wlen = len(word)
    if wlen > m * n:
        return False

    def dfs(i, j, k):
        if k == wlen:
            return True
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        tmp = board[i][j]
        board[i][j] = "#"
        found = (
            dfs(i + 1, j, k + 1)
            or dfs(i - 1, j, k + 1)
            or dfs(i, j + 1, k + 1)
            or dfs(i, j - 1, k + 1)
        )
        board[i][j] = tmp
        return found

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True
    return False


def main() -> None:
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
        board[i][j] = '#';
        bool found = dfs(i + 1, j, k + 1) || dfs(i - 1, j, k + 1) ||
                     dfs(i, j + 1, k + 1) || dfs(i, j - 1, k + 1);
        board[i][j] = tmp;
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
