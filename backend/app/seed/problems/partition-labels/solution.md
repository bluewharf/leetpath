## 思路

### 解法一（推荐）：最后出现位置 + 贪心切段

- 同一字母必须落在同一段，所以一段的右端至少要盖到段内每个字母的最后出现位置。
- 先扫一遍记下每个字母最后一次出现的下标。
- 再从左往右扫，维护当前段的 `end`：每遇到一个字母，就用它的最后位置扩张 `end`。
- 扫描下标走到 `end` 时，这一段已经无法再缩短，切一刀，长度是 `i - start + 1`。
- 贪心切尽可能多段：每次都在「必须覆盖」的最右边界切断。

### 解法二：字母区间合并

- 每个出现过的字母对应闭区间 `[首次, 末次]`，按左端排序后合并相交/包含的区间。
- 合并后每段长度即答案。与解法一等价：扫过的 `end` 就是在做区间合并。
- 字母表只有 26，排序可忽略；实现更「区间题」化，适合已经熟悉合并区间的人。

### 解法三：扩窗直到闭合

- 维护当前窗口内出现过的字母集合，反复把 `end` 扩到集合内每个字母的 last，直到 `end` 不再变再切。
- 不变量与解法一相同，但同一段可能被扫多次，更慢。
- 用来理解「窗口必须覆盖内部所有字母的最后一次出现」。

## 复杂度

- 解法一：时间 O(n)，空间 O(Σ)，字母表大小为 26
- 解法二：时间 O(n)，空间 O(Σ)（至多 26 个区间）
- 解法三：时间 O(n · Σ)，空间 O(Σ)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n").rstrip("\r")
    last = {c: i for i, c in enumerate(s)}
    start = end = 0
    parts: list[int] = []
    for i, c in enumerate(s):
        if last[c] > end:
            end = last[c]
        if i == end:
            parts.append(i - start + 1)
            start = i + 1
    print(" ".join(map(str, parts)))


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
    int last[26];
    memset(last, -1, sizeof(last));
    int n = (int)s.size();
    for (int i = 0; i < n; ++i) last[s[i] - 'a'] = i;
    int start = 0, end = 0;
    vector<int> parts;
    for (int i = 0; i < n; ++i) {
        end = max(end, last[s[i] - 'a']);
        if (i == end) {
            parts.push_back(i - start + 1);
            start = i + 1;
        }
    }
    for (int i = 0; i < (int)parts.size(); ++i) {
        if (i) cout << ' ';
        cout << parts[i];
    }
    cout << '\n';
    return 0;
}
```
