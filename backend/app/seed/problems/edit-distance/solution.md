## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：滚动数组 DP（推荐）
- `dp[i][j]` 表示 `word1` 前 `i` 个字符变成 `word2` 前 `j` 个字符的最少操作。
- 末字符相同则继承 `dp[i-1][j-1]`；否则在删除、插入、替换里取最小再加 1。
- 边界：空串互转的代价就是另一串的长度。只依赖上一行，滚动成 `prev/cur` 两行。
- 输入可能出现空行，按空串处理。模板即此写法。

### 解法二：完整二维表
- 开 `(n+1)×(m+1)` 的表，按同样转移填。空间 O(nm)，但回溯路径、打印操作序列时必须留整表。
- 时间同为 O(nm)，实现更直观，适合白板先画格子再压滚动。
- 本题只问距离，不必整表。

### 解法三：记忆化递归
- `dfs(i, j)` 从两个后缀（或前缀）出发，相同则前进，否则三维 `1+min(删, 插, 替)`，结果进缓存。
- 状态数仍是 O(nm)，时间同阶，但递归常数大、有栈深；空串边界要单独写。
- 适合先讲搜索再改循环；落地用解法一。

## 复杂度

- 解法一：时间 O(nm)，空间 O(m)（n=|word1|，m=|word2|）
- 解法二：时间 O(nm)，空间 O(nm)
- 解法三：时间 O(nm)，空间 O(nm)（缓存 + 递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：滚动 DP。dp[i][j] 是 word1 前 i 个变成 word2 前 j 个的最少操作。
import sys


def main() -> None:
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    lines = data.split("\n")
    w1 = lines[0] if lines else ""  # 空行按空串处理
    w2 = lines[1] if len(lines) > 1 else ""
    n, m = len(w1), len(w2)
    prev = list(range(m + 1))  # 空串变成 word2 前 j 个：插 j 次
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        cur[0] = i  # word1 前 i 个变成空串：删 i 次
        a = w1[i - 1]
        for j in range(1, m + 1):
            if a == w2[j - 1]:
                cur[j] = prev[j - 1]  # 末字符相同，免费继承
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])  # 删 / 插 / 替
        prev = cur
    print(prev[m])


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：滚动 DP。dp[i][j] 是 word1 前 i 个变成 word2 前 j 个的最少操作。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string w1, w2;
    if (!getline(cin, w1)) w1.clear();  // 空行按空串处理
    if (!getline(cin, w2)) w2.clear();
    if (!w1.empty() && w1.back() == '\r') w1.pop_back();
    if (!w2.empty() && w2.back() == '\r') w2.pop_back();
    int n = (int)w1.size(), m = (int)w2.size();
    vector<int> prev(m + 1);
    iota(prev.begin(), prev.end(), 0);  // 空串变成 word2 前 j 个：插 j 次
    for (int i = 1; i <= n; i++) {
        vector<int> cur(m + 1);
        cur[0] = i;  // word1 前 i 个变成空串：删 i 次
        char a = w1[i - 1];
        for (int j = 1; j <= m; j++) {
            if (a == w2[j - 1]) cur[j] = prev[j - 1];  // 末字符相同，免费继承
            else cur[j] = 1 + min({prev[j], cur[j - 1], prev[j - 1]});  // 删 / 插 / 替
        }
        prev.swap(cur);
    }
    cout << prev[m] << "\n";
    return 0;
}
```

