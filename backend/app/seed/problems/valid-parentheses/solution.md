## 思路

### 解法一（推荐）：栈 + 配对映射

- 用栈维护「还没配上的左括号」：遇左就压，遇右必须刚好弹到同类型的左。
- 右括号来时栈空，或栈顶不是它的配对，说明顺序错了或类型错了，立刻失败。
- 扫完栈必须空：剩下的都是没闭合的左括号。
- 映射写成 `右 → 左`，判断时只分「是不是右括号」两支，三种括号共用一套逻辑。

### 解法二：反复删除配对子串

- 循环把 `()`、`[]`、`{}` 从字符串里删掉，直到删不动；最终空串则合法。
- 正确，但不变量是「每次消掉最内层配对」，每轮扫描都是 O(n)，最坏 O(n²)。
- 与解法一差在：用多次改写字符串代替栈，面试里能过正确性，过不了效率追问。

### 解法三：只计数（反例）

- 单一括号可以用「左 +1、右 -1、过程中不为负、结束为 0」判断。
- 三种括号交叉如 `([)]` 计数全对但顺序非法，所以不能只用三个计数器。
- 用来说明本题必须记住「最近未匹配的左括号」，也就是栈。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n²)，空间 O(n)
- 解法三：时间 O(n)，空间 O(1)（仅对单一括号成立，本题不够）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
