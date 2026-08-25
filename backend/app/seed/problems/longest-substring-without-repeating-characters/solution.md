## 思路

### 解法一：滑动窗口 + 最近下标（推荐）

- 右端一路右移，窗口 `[start, i]` 内始终不含重复字符。
- 记下每个字符最近一次出现的下标；若再次出现且落在窗口内，左端一次跳到该下标的下一位。
- 每次更新后用 `i - start + 1` 刷新最长长度；左端只右移不回退，每个下标进出常数次。
- 空格、符号都是合法字符，读入只去掉行尾换行，不能 `strip`。
- 和「频次 while 收缩」比：重复出现时左端一步跳到位，少一层循环。

### 解法二：滑动窗口 + 频次

- 右端纳入字符，若某字符次数 > 1，左端 `while` 右移直到窗口再次无重复。
- 不变量同样是「窗口内各字符至多一次」，用数组/哈希计数即可。
- 左端可能连着移动多次，总次数仍 O(n)，和最小覆盖子串是同一套窗口模板。
- 字符集大时哈希常数略差，ASCII 可开 256 桶。

### 解法三：枚举左端 + 集合

- 固定左端，右端延伸直到出现重复，用集合维护当前段，更新答案。
- 每次从空集合重建，时间 O(n²)，用来对照「为何左端绝不能回退」。
- 数据稍大就会 TLE，只作正确性对照，不作为提交解。

## 复杂度

- 解法一：时间 O(n)，空间 O(Σ)（Σ 为字符集大小）
- 解法二：时间 O(n)，空间 O(Σ)
- 解法三：时间 O(n²)，空间 O(Σ)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：窗口 [start,i] 无重复；重复落在窗内则左端一次跳到 last[ch]+1。
import sys


def main() -> None:
    # 读入整行，只剥换行；空格/符号都是合法字符，不能 strip。
    s = sys.stdin.readline()
    if s.endswith("\n"):
        s = s[:-1]
    if s.endswith("\r"):
        s = s[:-1]
    last: dict[str, int] = {}  # 每个字符最近一次出现的下标
    start = 0  # 窗口 [start, i] 内无重复
    best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            # 重复落在窗口内：左端一次跳到该下标之后，左端只右移不回退。
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    print(best)


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：窗口 [start,i] 无重复；重复落在窗内则左端一次跳到 last[ch]+1。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    int last[256];
    memset(last, -1, sizeof(last));  // -1 表示从未出现，不会误判在窗口内
    int start = 0, best = 0;  // 窗口 [start, i] 无重复
    for (int i = 0; i < (int)s.size(); i++) {
        unsigned char ch = (unsigned char)s[i];
        if (last[ch] >= start) start = last[ch] + 1;  // 重复在窗内才跳左端
        last[ch] = i;
        best = max(best, i - start + 1);
    }
    cout << best << "\n";
    return 0;
}
```
