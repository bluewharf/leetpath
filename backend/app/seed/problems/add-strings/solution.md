## 思路

从尾向前按位相加，维护进位。不要 `int()` 整串，会溢出。

### 解法一（推荐）：双指针从低位加

- `i`、`j` 从末尾往前，缺位当 0，`carry` 参与加法。
- 结果按低位到高位收集，最后反转；注意去掉前导零，全 0 留一个 `0`。
- `"0"+"0"`、一长一短、最高位进位都要覆盖。

### 解法二：先补齐再逐位

- 把短串左侧补 0 对齐再加，和笔算一致，代码稍长。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def add_strings(a: str, b: str) -> str:
    if a == "":
        a = "0"
    if b == "":
        b = "0"
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        x = ord(a[i]) - 48 if i >= 0 else 0
        y = ord(b[j]) - 48 if j >= 0 else 0
        s = x + y + carry
        out.append(str(s % 10))
        carry = s // 10
        i -= 1
        j -= 1
    while len(out) > 1 and out[-1] == "0":
        out.pop()
    return "".join(reversed(out))


def main() -> None:
    a = sys.stdin.readline()
    b = sys.stdin.readline()
    a = a[:-1] if a.endswith("\n") else a
    b = b[:-1] if b.endswith("\n") else b
    print(add_strings(a, b))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string add_strings(string a, string b) {
    if (a.empty()) a = "0";
    if (b.empty()) b = "0";
    int i = (int)a.size() - 1, j = (int)b.size() - 1, carry = 0;
    string out;
    while (i >= 0 || j >= 0 || carry) {
        int x = i >= 0 ? a[i] - '0' : 0;
        int y = j >= 0 ? b[j] - '0' : 0;
        int s = x + y + carry;
        out.push_back(char('0' + s % 10));
        carry = s / 10;
        --i;
        --j;
    }
    while (out.size() > 1 && out.back() == '0') out.pop_back();
    reverse(out.begin(), out.end());
    return out;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string a, b;
    getline(cin, a);
    getline(cin, b);
    cout << add_strings(a, b) << '\n';
    return 0;
}
```
