## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：数字栈 + 字符串栈（推荐）
- 遇到 `[` 把当前倍数和已拼好的前缀压栈，括号内从空白重新拼。
- 遇到 `]` 弹出倍数 `k` 和前缀，把括号内串重复 `k` 次接到前缀后面。
- 数字可能有多位，用 `k = k * 10 + d` 累加，入栈后清零；字母直接追加到当前串。
- 输入保证括号匹配、数字只表示倍数，扫完当前串就是解码结果。模板即此写法。

### 解法二：递归下降
- 维护全局下标 `i`：读数字得到 `k`，遇 `[` 递归解析内部，遇 `]` 返回当前片段，字母直接拼上。
- 与栈解法一一对应：递归调用栈就是「前缀 / 倍数」栈，嵌套层数即递归深度。
- 时间仍由输出长度主导；空间是递归深度（嵌套层数），对很深的括号不如显式栈稳。
- 文法讲得清时很好用；落地仍推荐解法一，边界（多位数字、连续括号）更好盯。

## 复杂度

- 解法一：时间 O(L)，空间 O(L)（L 为解码后长度）
- 解法二：时间 O(L)，空间 O(L)（输出 + 递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
