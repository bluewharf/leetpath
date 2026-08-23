## 思路

- 用栈拆嵌套：遇到 `[` 把当前倍数和已拼好的前缀压栈，括号内从空白重新拼。
- 遇到 `]` 弹出倍数 `k` 和前缀，把括号内串重复 `k` 次接到前缀后面。
- 数字可能有多位，用 `k = k * 10 + d` 累加，入栈后清零。
- 字母直接追加到当前串。
- 输入保证括号匹配、数字只表示倍数，扫完当前串就是解码结果。

## 复杂度

- 时间：O(L)，L 为解码后长度
- 空间：O(L)

## 模板代码

### Python3

```python
import sys


def decode_string(s: str) -> str:
    num_stack = []
    str_stack = []
    cur = []
    k = 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + ord(ch) - 48
        elif ch == "[":
            num_stack.append(k)
            str_stack.append(cur)
            cur = []
            k = 0
        elif ch == "]":
            prev = str_stack.pop()
            n = num_stack.pop()
            cur = prev + cur * n
        else:
            cur.append(ch)
    return "".join(cur)


def main() -> None:
    s = sys.stdin.readline().rstrip("\r\n")
    print(decode_string(s))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string decode_string(const string& s) {
    vector<int> num_stack;
    vector<string> str_stack;
    string cur;
    int k = 0;
    for (char ch : s) {
        if (ch >= '0' && ch <= '9') {
            k = k * 10 + (ch - '0');
        } else if (ch == '[') {
            num_stack.push_back(k);
            str_stack.push_back(cur);
            cur.clear();
            k = 0;
        } else if (ch == ']') {
            string prev = str_stack.back();
            str_stack.pop_back();
            int n = num_stack.back();
            num_stack.pop_back();
            string inner = cur;
            cur = prev;
            for (int i = 0; i < n; i++) cur += inner;
        } else {
            cur.push_back(ch);
        }
    }
    return cur;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    cout << decode_string(s) << "\n";
    return 0;
}
```
