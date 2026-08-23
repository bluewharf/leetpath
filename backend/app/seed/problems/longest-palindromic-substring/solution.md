## 思路

- 回文由中心决定：每个位置做奇数中心 `(i,i)` 和偶数中心 `(i,i+1)`，向外扩到两边字符不等。
- 一次扩展得到该中心能撑到的最长回文；全局取最长，长度相同再取字典序更小者（题面要求确定性输出）。
- 共 `2n-1` 个中心，每个最多扩 `n` 步，`n ≤ 1000` 时 O(n²) 足够。
- 空串直接输出空行；单字符本身就是回文，作为初始答案。

## 复杂度

- 时间：O(n²)
- 空间：O(1)（不计答案串）

## 模板代码

### Python3

```python
import sys


def expand(s: str, l: int, r: int) -> str:
    n = len(s)
    while l >= 0 and r < n and s[l] == s[r]:
        l -= 1
        r += 1
    return s[l + 1 : r]


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    if not s:
        print()
        return
    best = s[0]
    n = len(s)
    for i in range(n):
        for pal in (expand(s, i, i), expand(s, i, i + 1)):
            if len(pal) > len(best) or (len(pal) == len(best) and pal < best):
                best = pal
    print(best)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string expand(const string& s, int l, int r) {
    int n = (int)s.size();
    while (l >= 0 && r < n && s[l] == s[r]) {
        l--;
        r++;
    }
    return s.substr(l + 1, r - l - 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (s.empty()) {
        cout << "\n";
        return 0;
    }
    string best = s.substr(0, 1);
    int n = (int)s.size();
    for (int i = 0; i < n; i++) {
        string odd = expand(s, i, i);
        string even = expand(s, i, i + 1);
        for (const string& pal : {odd, even}) {
            if ((int)pal.size() > (int)best.size() ||
                (pal.size() == best.size() && pal < best)) {
                best = pal;
            }
        }
    }
    cout << best << "\n";
    return 0;
}
```
