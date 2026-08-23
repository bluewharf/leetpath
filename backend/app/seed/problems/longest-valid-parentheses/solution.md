## 思路

- 栈里存下标，栈底恒放一个哨兵，表示「当前无效段」的左边界（初始为 `-1`）。
- 遇 `'('` 把下标入栈；遇 `')'` 先弹出一个：若栈空，这个多出来的 `')'` 成为新哨兵。
- 栈非空时，当前 `')'` 与栈顶下标之间的距离就是一段合法括号的长度。
- 哨兵把断开位置钉住，保证统计的是连续子串，不会跨过无法匹配的括号。
- 嵌套（`(()())`）和相邻拼接（`()()`）都被「弹出后看栈顶」这一种更新覆盖。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

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
