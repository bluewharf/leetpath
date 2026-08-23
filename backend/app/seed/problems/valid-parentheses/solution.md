## 思路

- 用栈维护「还没配上的左括号」：遇左就压，遇右必须刚好弹到同类型的左。
- 右括号来时栈空，或栈顶不是它的配对，说明顺序错了或类型错了，立刻失败。
- 扫完栈必须空：剩下的都是没闭合的左括号。
- 映射写成 `右 → 左`，判断时只分「是不是右括号」两支，三种括号共用一套逻辑。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []
    for c in s:
        if c in pairs:
            if not st or st[-1] != pairs[c]:
                return False
            st.pop()
        else:
            st.append(c)
    return not st


def main() -> None:
    s = sys.stdin.readline().rstrip("\r\n")
    print("true" if is_valid(s) else "false")


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
    if (!(cin >> s)) {
        cout << "true\n";
        return 0;
    }
    unordered_map<char, char> pairs{{')', '('}, {']', '['}, {'}', '{'}};
    string st;
    for (char c : s) {
        auto it = pairs.find(c);
        if (it != pairs.end()) {
            if (st.empty() || st.back() != it->second) {
                cout << "false\n";
                return 0;
            }
            st.pop_back();
        } else {
            st.push_back(c);
        }
    }
    cout << (st.empty() ? "true" : "false") << "\n";
    return 0;
}
```
