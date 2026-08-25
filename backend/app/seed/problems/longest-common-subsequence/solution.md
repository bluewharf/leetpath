## 思路

### 解法一：滚动数组 DP（推荐）

- 状态仍是「`text1` 前 `i` 个与 `text2` 前 `j` 个的 LCS 长度」，第 `i` 行只依赖第 `i-1` 行，用 `prev` / `cur` 两行滚动。
- 当前字符相等：这对匹配一定接在两边都缩短一位的 LCS 后面，`cur[j] = prev[j-1] + 1`；必须先读上一行左邻，所以不能在同一行里从左到右原地覆盖。
- 不相等：答案只能丢掉 `text1` 当前字符或丢掉 `text2` 当前字符，`cur[j] = max(prev[j], cur[j-1])`。
- 空前缀对应全 0，第一行/第一列不必特判；模板按第二维滚动，空间 `O(m)`，先交换使较短串做内层可到 `O(min(n,m))`。
- 和完整二维表比：转移一模一样，只是不保留整张表；本题只求长度，滚动即可。

### 解法二：二维 DP

- `dp[i][j]` 显式存整张表，转移与解法一相同，填表时能直接看出每个前缀对的答案。
- `i`、`j` 从小到大填；若还要回溯打印一条具体 LCS，必须留二维表（或额外前驱）。
- 只求长度时多占一层 `O(nm)` 空间，默写比滚动数组更直观，适合先写对再压缩。

### 解法三：递归 + 记忆化

- `f(i,j)` 定义为从下标 `i`、`j` 往后的 LCS：字符相等则 `1 + f(i+1,j+1)`，否则 `max(f(i+1,j), f(i,j+1))`。
- 无记忆化会把重叠子问题打成指数；用数组/哈希记忆后时间仍 `O(nm)`，递归栈 `O(n+m)`。
- 更贴近「定义即转移」，但常被卡栈、常数也更大，提交用解法一。

## 复杂度

- 解法一：时间 O(nm)，空间 O(m)（按第二维滚动；交换两串后可到 O(min(n,m))）
- 解法二：时间 O(nm)，空间 O(nm)
- 解法三：时间 O(nm)，空间 O(nm)（记忆）+ O(n+m)（递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：滚动 DP。prev[j] 是 s1 前 i-1 与 s2 前 j 的 LCS；相等必须用左上。
import sys


def main() -> None:
    # 读入：两行字符串，均可为空；只剥末尾换行，不能 split() 把空行吃掉。
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    lines = data.split("\n")
    s1 = lines[0] if lines else ""
    s2 = lines[1] if len(lines) > 1 else ""
    n, m = len(s1), len(s2)
    # 不变量：prev[j] = s1 前 i-1 个与 s2 前 j 个的 LCS 长度；空前缀全 0。
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        a = s1[i - 1]
        for j in range(1, m + 1):
            if a == s2[j - 1]:
                # 配对必须接「两边都缩短 1」，只能读上一行左邻 prev[j-1]。
                cur[j] = prev[j - 1] + 1
            else:
                # 丢掉 s1 当前字符或丢掉 s2 当前字符，取较长者。
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    print(prev[m])


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：滚动 DP。prev[j] 是 s1 前 i-1 与 s2 前 j 的 LCS；相等必须用左上。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s1, s2;
    getline(cin, s1);  // 两行均可为空串
    getline(cin, s2);
    int n = (int)s1.size(), m = (int)s2.size();
    // 不变量：prev[j] = s1 前 i-1 个与 s2 前 j 个的 LCS；空前缀为 0。
    vector<int> prev(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        vector<int> cur(m + 1, 0);
        char a = s1[i - 1];
        for (int j = 1; j <= m; j++) {
            if (a == s2[j - 1]) cur[j] = prev[j - 1] + 1;  // 必须用左上，不能原地覆盖
            else cur[j] = prev[j] >= cur[j - 1] ? prev[j] : cur[j - 1];
        }
        prev.swap(cur);
    }
    cout << prev[m] << "\n";
    return 0;
}
```
