## 思路

- 二维 DP：`dp[i][j]` 表示 `text1` 前 `i` 个字符与 `text2` 前 `j` 个字符的 LCS 长度。
- 当前字符相等时，这对字符一定可以接在「两边都缩短一位」的 LCS 后面，即 `dp[i-1][j-1]+1`。
- 不相等时，答案只能来自丢掉 `text1` 当前字符或丢掉 `text2` 当前字符，取 `max(dp[i-1][j], dp[i][j-1])`。
- 任意公共子序列的最后一个匹配，要么用到这对相等字符，要么至少有一边没用到当前位置，因此转移覆盖全部情况。
- 第一行/第一列对应空前缀，自然为 0；滚动数组只需上一行，空间可压到 `O(min(n,m))`。

## 复杂度

- 时间：O(nm)
- 空间：O(min(n, m))

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    lines = data.split("\n")
    s1 = lines[0] if lines else ""
    s2 = lines[1] if len(lines) > 1 else ""
    n, m = len(s1), len(s2)
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        a = s1[i - 1]
        for j in range(1, m + 1):
            if a == s2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    print(prev[m])


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
    string s1, s2;
    getline(cin, s1);
    getline(cin, s2);
    int n = (int)s1.size(), m = (int)s2.size();
    vector<int> prev(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        vector<int> cur(m + 1, 0);
        char a = s1[i - 1];
        for (int j = 1; j <= m; j++) {
            if (a == s2[j - 1]) cur[j] = prev[j - 1] + 1;
            else cur[j] = prev[j] >= cur[j - 1] ? prev[j] : cur[j - 1];
        }
        prev.swap(cur);
    }
    cout << prev[m] << "\n";
    return 0;
}
```
