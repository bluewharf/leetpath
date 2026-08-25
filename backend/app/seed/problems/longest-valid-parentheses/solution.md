## 思路

### 解法一：栈存下标 + 哨兵（推荐）

- 栈里存下标，栈底恒放哨兵，表示「当前无效段」的左边界（初始为 `-1`）。
- 遇 `'('` 把下标入栈；遇 `')'` 先弹出：若栈空，这个多出来的 `')'` 成为新哨兵。
- 栈非空时，当前 `')'` 与栈顶下标之间的距离就是一段合法括号的长度。
- 哨兵把断开位置钉住，统计的是连续子串，不会跨过无法匹配的括号。
- 嵌套（`(()())`）和相邻拼接（`()()`）都被「弹出后看栈顶」这一种更新覆盖。

### 解法二：DP

- `dp[i]` 表示以位置 `i` 结尾的最长有效括号长度；以 `'('` 结尾必为 0。
- `s[i]` 为 `')'` 时分两类：前一个是 `'('`，则 `dp[i] = dp[i-2] + 2`；前一个也是 `')'`，则看 `i - dp[i-1] - 1` 是否为 `'('`，是则再接上 `dp[i-1] + 2` 以及该 `'('` 之前的 `dp`。
- 和第二类漏写「再接前面一段」就会把 `()()` 算成 2。时间和栈法同阶，转移分类比哨兵栈更碎。

### 解法三：左右各扫一遍计数

- 从左到右记 `left`/`right` 括号数，相等时更新长度；`right > left` 则清零（多出的右括号切断连续段）。
- 再从右到左对称扫一遍，处理「左括号一直偏多」的前缀（如 `(()`）。
- 空间 O(1)，但必须两遍；漏掉反向扫描会错。和栈法差在用计数代替下标匹配。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    best = 0
    st = [-1]
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
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
    int best = 0;
    vector<int> st;
    st.push_back(-1);
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') {
            st.push_back(i);
        } else {
            st.pop_back();
            if (st.empty()) st.push_back(i);
            else best = max(best, i - st.back());
        }
    }
    cout << best << "\n";
    return 0;
}
```
