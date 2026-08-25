## 思路

### 解法一（推荐）：预处理回文表 + 回溯切分

- 切分位置的回溯：从 `start` 枚举右端点 `end`，只有 `s[start..end]` 是回文才切一刀、递归后面。
- 预处理 `pal[i][j]`：长度 1/2 看两端字符，更长则两端相同且内部已经是回文，判断从 O(n) 降到 O(1)。
- 切到 `start == n` 时收一种方案，回溯弹栈。
- 各段用空格拼成一行，全部收集后按字典序排序再输出，保证多解顺序确定。
- `|s| ≤ 16`，切法最多 `2^{n-1}`，可以全枚举。

### 解法二：中心扩展即时判断

- 不建 `n × n` 表，每次尝试切分时用双指针向内扩判断该段是否回文。
- 单次判断从 O(1) 变 O(段长)，总时间多一个线性因子。
- 空间少一张表；`n` 很小时与解法一难分胜负，更长的串就该预处理。

### 解法三：DP 记录所有合法切法

- `dp[i]` 存把 `s[i:]` 切成回文段的全部方案；转移枚举第一个回文前缀。
- 本质仍是搜索，只是改成自底向上；输出同样要按字典序排序。
- 实现比回溯重，适合已经在写「分割回文串 II」（最少刀数）时对照。

## 复杂度

- 解法一：时间 O(n · 2^n)（预处理 O(n²)，每种切法再花线性时间拼串），空间 O(n²)（回文表）+ O(n)（递归栈）
- 解法二：时间 O(n² · 2^n) 量级，空间 O(n)
- 解法三：时间 O(n · 2^n)，空间 O(n · 2^n)（存全部方案）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n").rstrip("\r")
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = (s[i] == s[j]) and (j - i < 2 or pal[i + 1][j - 1])
    ans: list[str] = []
    path: list[str] = []

    def dfs(start: int) -> None:
        if start == n:
            ans.append(" ".join(path))
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start : end + 1])
                dfs(end + 1)
                path.pop()

    dfs(0)
    ans.sort()
    sys.stdout.write("\n".join(ans))
    if ans:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string s;
int n;
vector<vector<char>> pal;
vector<string> path, ans;

void dfs(int start) {
    if (start == n) {
        string line;
        for (int i = 0; i < (int)path.size(); ++i) {
            if (i) line.push_back(' ');
            line += path[i];
        }
        ans.push_back(line);
        return;
    }
    for (int end = start; end < n; ++end) {
        if (pal[start][end]) {
            path.push_back(s.substr(start, end - start + 1));
            dfs(end + 1);
            path.pop_back();
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    getline(cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    n = (int)s.size();
    pal.assign(n, vector<char>(n, 0));
    for (int i = n - 1; i >= 0; --i) {
        for (int j = i; j < n; ++j) {
            pal[i][j] = (s[i] == s[j]) && (j - i < 2 || pal[i + 1][j - 1]);
        }
    }
    dfs(0);
    sort(ans.begin(), ans.end());
    for (const auto& line : ans) cout << line << '\n';
    return 0;
}
```
