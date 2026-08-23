## 思路

- 二维 DP：`dp[i][j]` 表示 `word1` 前 `i` 个字符变成 `word2` 前 `j` 个字符的最少操作。
- 末字符相同则直接继承 `dp[i-1][j-1]`；否则在删除、插入、替换里取最小再加 1。
- 边界：空串互转的代价就是另一串的长度。
- 只依赖上一行，滚动成 `prev/cur` 两行即可。
- 输入可能出现空行，按空串处理。

## 复杂度

- 时间：O(|word1| · |word2|)
- 空间：O(|word2|)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    lines = data.split("\n")
    w1 = lines[0] if lines else ""
    w2 = lines[1] if len(lines) > 1 else ""
    n, m = len(w1), len(w2)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        cur[0] = i
        a = w1[i - 1]
        for j in range(1, m + 1):
            if a == w2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
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
    string w1, w2;
    if (!getline(cin, w1)) w1.clear();
    if (!getline(cin, w2)) w2.clear();
    if (!w1.empty() && w1.back() == '\r') w1.pop_back();
    if (!w2.empty() && w2.back() == '\r') w2.pop_back();
    int n = (int)w1.size(), m = (int)w2.size();
    vector<int> prev(m + 1);
    iota(prev.begin(), prev.end(), 0);
    for (int i = 1; i <= n; i++) {
        vector<int> cur(m + 1);
        cur[0] = i;
        char a = w1[i - 1];
        for (int j = 1; j <= m; j++) {
            if (a == w2[j - 1]) cur[j] = prev[j - 1];
            else cur[j] = 1 + min({prev[j], cur[j - 1], prev[j - 1]});
        }
        prev.swap(cur);
    }
    cout << prev[m] << "\n";
    return 0;
}
```
