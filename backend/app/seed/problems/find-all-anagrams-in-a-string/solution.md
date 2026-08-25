## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：定长滑窗 + 26 计数（推荐）
- 窗口长度等于 `|p|`，比的是 26 个小写字母的计数是否完全一致。
- 先统计 `p` 的目标计数，再用 `s` 的前 `|p|` 个字符填满窗口。
- 每次右端进一个、左端出一个，计数相等就把左端下标记下来。
- `|s| < |p|` 时不可能有异位词，直接空答案；从左往右滑，下标天然升序。模板即此写法。

### 解法二：每个窗口排序后比较
- 对每个起点把长度为 `|p|` 的子串排序，与排好序的 `p` 比是否相等。
- 正确但每个窗口要 O(|p| log |p|)，总时间 O(|s| · |p| log |p|)，`s` 稍长就会慢。
- 不必自己维护计数差分，适合口头验算或数据极小；正式提交用解法一。
- 变体：窗口字符排序当哈希键，本质仍是 O(|p| log |p|) 每次。

## 复杂度

- 解法一：时间 O(|s|)，空间 O(1)（不计答案；字母计数固定 26）
- 解法二：时间 O(|s| · |p| log |p|)，空间 O(|p|)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：定长滑窗。窗口长度 |p|，26 计数与 p 完全一致即为异位词。
import sys


def main() -> None:
    lines = sys.stdin.read().splitlines()
    s = lines[0] if len(lines) > 0 else ""
    p = lines[1] if len(lines) > 1 else ""
    ns, np = len(s), len(p)
    if np == 0 or ns < np:
        print()  # 窗口都铺不满，不可能有异位词
        return
    need = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    win = [0] * 26
    for i in range(np):
        win[ord(s[i]) - 97] += 1
    ans = []
    if win == need:
        ans.append(0)
    for i in range(np, ns):
        win[ord(s[i]) - 97] += 1  # 右端进一个、左端出一个
        win[ord(s[i - np]) - 97] -= 1
        if win == need:
            ans.append(i - np + 1)  # 记下窗口左端下标
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：定长滑窗。窗口长度 |p|，26 计数与 p 完全一致即为异位词。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, p;
    if (!getline(cin, s)) s.clear();
    if (!getline(cin, p)) p.clear();
    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!p.empty() && p.back() == '\r') p.pop_back();
    int ns = (int)s.size(), np = (int)p.size();
    if (np == 0 || ns < np) {
        cout << "\n";  // 窗口都铺不满，不可能有异位词
        return 0;
    }
    array<int, 26> need{}, win{};
    for (char ch : p) need[ch - 'a']++;
    for (int i = 0; i < np; i++) win[s[i] - 'a']++;
    vector<int> ans;
    if (win == need) ans.push_back(0);
    for (int i = np; i < ns; i++) {
        win[s[i] - 'a']++;  // 右端进一个、左端出一个
        win[s[i - np] - 'a']--;
        if (win == need) ans.push_back(i - np + 1);  // 记下窗口左端下标
    }
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << " ";
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
```

