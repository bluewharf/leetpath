## 思路

- 最短覆盖子串是典型的「先扩张再收缩」滑动窗口：右指针纳入字符，直到窗口已经覆盖 `t` 的全部需求（含重复次数）。
- 用 `need` 记 `t` 各字符配额，`formed` 记「当前已满足配额的字符种类数」；`formed == required` 时窗口合法。
- 合法后左指针尽量右移：每丢掉一个字符，若某种需求字符数量掉到配额以下，窗口立刻非法，停止收缩。
- 收缩过程中记下最短窗口的左右端；扫完若不存在合法窗口则输出空行。
- 每个下标最多进、出窗口一次，所以是线性的。

## 复杂度

- 时间：O(|s| + |t|)
- 空间：O(字符集)，本题为大小写字母

## 模板代码

### Python3

```python
import sys
from collections import Counter


def main():
    s = sys.stdin.readline().rstrip("\n")
    t = sys.stdin.readline().rstrip("\n")
    need = Counter(t)
    required = len(need)
    formed = 0
    window = {}
    left = 0
    best_len = 10**18
    best_l = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1
        while left <= right and formed == required:
            cur = right - left + 1
            if cur < best_len:
                best_len = cur
                best_l = left
            cl = s[left]
            window[cl] -= 1
            if cl in need and window[cl] < need[cl]:
                formed -= 1
            left += 1
    if best_len == 10**18:
        print()
    else:
        print(s[best_l : best_l + best_len])


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
    string s, t;
    getline(cin, s);
    getline(cin, t);
    int need[128] = {};
    int window[128] = {};
    int required = 0;
    for (unsigned char c : t) {
        if (need[c] == 0) required++;
        need[c]++;
    }
    int formed = 0;
    int best_len = INT_MAX, best_l = 0;
    int left = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        unsigned char ch = s[right];
        window[ch]++;
        if (need[ch] && window[ch] == need[ch]) formed++;
        while (left <= right && formed == required) {
            if (right - left + 1 < best_len) {
                best_len = right - left + 1;
                best_l = left;
            }
            unsigned char cl = s[left];
            window[cl]--;
            if (need[cl] && window[cl] < need[cl]) formed--;
            left++;
        }
    }
    if (best_len == INT_MAX) cout << '\n';
    else cout << s.substr(best_l, best_len) << '\n';
    return 0;
}
```
