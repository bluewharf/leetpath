## 思路

按竖式：`num1[i] * num2[j]` 加到结果数组下标 `i+j`（从低位对齐）。先写对朴素，不必上 FFT。

### 解法一（推荐）：数组存每位

- 令 `num1`、`num2` 从高到低，对应低位下标 `n1-1-i`、`n2-1-j`。
- 开长度 `n1+n2` 的数组，积加到 `pos[i+j]`，再统一处理进位。
- 去掉前导零；任一方为 `0` 直接回 `0`。
- 先问正负号：本题非负。

### 解法二：用大数加法累加部分积

- 对 `num2` 每一位乘 `num1` 再左移若干位，用字符串加法累加。
- 正确但常数差，代码更长。

## 复杂度

- 解法一：时间 O(nm)，空间 O(n+m)
- 解法二：时间 O(nm)，空间 O(n+m)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def multiply(a: str, b: str) -> str:
    a = a.strip()
    b = b.strip()
    if a == "0" or b == "0":
        return "0"
    n, m = len(a), len(b)
    pos = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            pos[(n - 1 - i) + (m - 1 - j)] += (ord(a[i]) - 48) * (ord(b[j]) - 48)
    carry = 0
    for k in range(len(pos)):
        s = pos[k] + carry
        pos[k] = s % 10
        carry = s // 10
    while carry:
        pos.append(carry % 10)
        carry //= 10
    while len(pos) > 1 and pos[-1] == 0:
        pos.pop()
    return "".join(str(d) for d in reversed(pos))


def main() -> None:
    a = sys.stdin.readline()
    b = sys.stdin.readline()
    print(multiply(a, b))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string multiply(string a, string b) {
    while (!a.empty() && isspace(a.back())) a.pop_back();
    while (!b.empty() && isspace(b.back())) b.pop_back();
    if (a == "0" || b == "0") return "0";
    int n = (int)a.size(), m = (int)b.size();
    vector<int> pos(n + m, 0);
    for (int i = n - 1; i >= 0; --i)
        for (int j = m - 1; j >= 0; --j)
            pos[(n - 1 - i) + (m - 1 - j)] += (a[i] - '0') * (b[j] - '0');
    int carry = 0;
    for (int k = 0; k < (int)pos.size(); ++k) {
        int s = pos[k] + carry;
        pos[k] = s % 10;
        carry = s / 10;
    }
    while (carry) {
        pos.push_back(carry % 10);
        carry /= 10;
    }
    while (pos.size() > 1 && pos.back() == 0) pos.pop_back();
    string out;
    for (int i = (int)pos.size() - 1; i >= 0; --i) out.push_back(char('0' + pos[i]));
    return out;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string a, b;
    getline(cin, a);
    getline(cin, b);
    cout << multiply(a, b) << '\n';
    return 0;
}
```
