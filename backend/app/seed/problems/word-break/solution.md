## 思路

- 布尔 DP：`dp[i]` 表示前缀 `s[:i]` 能否拆成字典单词；`dp[0] = True` 表示空前缀可拆。
- 转移：枚举切点 `j < i`，若 `dp[j]` 为真且 `s[j:i]` 在字典里，则 `dp[i] = True`，可提前 break。
- 字典放进集合，判断子串是否成词是平均 O(1)；单词可重复使用，所以不需要「用过就删」。
- 不必要求字典词全部出现，只问 `s` 能不能被覆盖，看 `dp[n]` 即可。
- 失败的切分不会污染后面：只有某个前缀已经能拆，才允许从那里再接一个词。

## 复杂度

- 时间：O(n² · L)，L 为子串拷贝/哈希长度（n ≤ 300 足够）
- 空间：O(n + 字典总长)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    m = int(sys.stdin.readline())
    words = set()
    for _ in range(m):
        words.add(sys.stdin.readline().rstrip("\n"))
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    print("true" if dp[n] else "false")


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
    string s;
    cin >> s;
    int m;
    cin >> m;
    unordered_set<string> words;
    words.reserve(m * 2);
    for (int i = 0; i < m; i++) {
        string w;
        cin >> w;
        words.insert(w);
    }
    int n = (int)s.size();
    vector<char> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j] && words.count(s.substr(j, i - j))) {
                dp[i] = 1;
                break;
            }
        }
    }
    cout << (dp[n] ? "true" : "false") << "\n";
    return 0;
}
```
