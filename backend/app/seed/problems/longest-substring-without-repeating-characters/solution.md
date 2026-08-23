## 思路

- 滑动窗口：右端一路右移，窗口 `[start, i]` 内始终不含重复字符。
- 记下每个字符最近一次出现的下标；若再次出现且落在窗口内，把左端跳到该下标的下一位。
- 每次更新窗口后，用 `i - start + 1` 刷新最长长度。
- 左端只右移不回退，每个下标进出窗口常数次，因此线性。
- 空格、符号都是合法字符，读入时只能去掉行尾换行，不能 `strip`。

## 复杂度

- 时间：O(n)
- 空间：O(Σ)，Σ 为字符集大小

## 模板代码

### Python3

```python
import sys


def main() -> None:
    s = sys.stdin.readline()
    if s.endswith("\n"):
        s = s[:-1]
    if s.endswith("\r"):
        s = s[:-1]
    last: dict[str, int] = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    print(best)


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
    getline(cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    int last[256];
    memset(last, -1, sizeof(last));
    int start = 0, best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        unsigned char ch = (unsigned char)s[i];
        if (last[ch] >= start) start = last[ch] + 1;
        last[ch] = i;
        best = max(best, i - start + 1);
    }
    cout << best << "\n";
    return 0;
}
```
