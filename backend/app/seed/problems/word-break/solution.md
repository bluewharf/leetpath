## 思路

### 解法一（推荐）：前缀布尔 DP

- `dp[i]` 表示前缀 `s[:i]` 能否拆成字典单词；`dp[0] = True` 表示空前缀可拆。
- 转移：枚举切点 `j < i`，若 `dp[j]` 为真且 `s[j:i]` 在字典里，则 `dp[i] = True`，可提前 break。
- 字典放进集合，判断子串是否成词是平均 O(1)；单词可重复使用，所以不需要「用过就删」。
- 不必要求字典词全部出现，只问 `s` 能不能被覆盖，看 `dp[n]` 即可。
- 失败的切分不会污染后面：只有某个前缀已经能拆，才允许从那里再接一个词。

### 解法二：记忆化 DFS

- `dfs(i)` 问从下标 `i` 走到末尾能否拆完；枚举字典里每个词，若 `s` 从 i 起匹配该词，则递归 `i + len(word)`。
- 用数组记下 `i` 的成败，避免同一起点被重复搜索。
- 与解法一差在：按「下一个词」展开，而不是按「前缀切点」填表；字典词很少、词长短时分支更少。

### 解法三：BFS 切分位置

- 队列里放「当前已经匹配到的下标」，从 0 出发；每次尝试接一个字典词，新下标未访问过再入队。
- 到达 `n` 则成功。`visited` 防止同一位置重复入队，本质仍是 `dp[i]`。
- 与 DP 等价，只是用队列代替下标从小到大的循环，适合讲成「最短/任意可达」。

## 复杂度

- 解法一：时间 O(n² · L)，空间 O(n + 字典总长)，L 为子串拷贝/哈希长度
- 解法二：时间 O(n² · L) 或 O(n · 字典词数 · 词长)，空间 O(n + 字典总长)
- 解法三：时间 O(n² · L) 或 O(n · 字典词数 · 词长)，空间 O(n + 字典总长)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    # 读入：一行 s，一行 m，随后 m 个字典词
    s = sys.stdin.readline().rstrip("\n")
    m = int(sys.stdin.readline())
    words = set()
    for _ in range(m):
        words.add(sys.stdin.readline().rstrip("\n"))
    n = len(s)
    # dp[i]：前缀 s[:i] 能否拆成字典词；空前缀可拆
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break  # 单词可重复用，集合不删；找到一种切法即可
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
    // 读入：s、词数 m、m 个词
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
    // dp[i]：前 i 个字符能否拆完；dp[0] 空前缀为真
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
