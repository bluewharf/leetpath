## 思路

### 解法一：滑动窗口 + 配额计数（推荐）

- 最短覆盖子串是「先扩张再收缩」：右指针纳入字符，直到窗口覆盖 `t` 的全部需求（含重复次数）。
- `need` 记 `t` 各字符配额，`formed` 记「当前已满足配额的字符种类数」；`formed == required` 时窗口合法。
- 合法后左指针尽量右移：丢掉的需求字符掉到配额以下则窗口立刻非法，停止收缩。
- 收缩过程中记下最短窗口的左右端；不存在合法窗口则输出空行。
- 每个下标最多进出一次，因此线性；和「无重复最长子串」差在合法条件是「种类配额凑齐」而不是「无重复」。

### 解法二：过滤关键位置再滑窗

- 先收集 `s` 中属于 `t` 字符集的下标，再在这条「关键序列」上做同样的配额窗口。
- `s` 很长而 `t` 字符很稀时常数更好，最坏仍 O(|s|+|t|)。
- 还原答案时用原串下标切片；和解法一差在窗口右端改成关键下标，逻辑不变。

### 解法三：按左端枚举 + 欠账

- 固定左端，右端只增不减地扩张到覆盖，再把左端右移时把欠账加回去。
- 本质仍是双指针；写成两层 for 且把左端重置就会退化成 O(|s|²)。
- 用来强调「左端绝不能回退」，提交仍用解法一。

## 复杂度

- 解法一：时间 O(|s|+|t|)，空间 O(Σ)（本题为大小写字母）
- 解法二：时间 O(|s|+|t|)，空间 O(|s|+Σ)
- 解法三：时间 O(|s|+|t|)（正确的双指针）或 O(|s|²)（左端回退），空间 O(Σ)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
