## 思路

### 解法一：中心扩展（推荐）

- 回文由中心决定：每个位置做奇数中心 `(i,i)` 和偶数中心 `(i,i+1)`，向外扩到两边字符不等。
- 一次扩展得到该中心能撑到的最长回文；全局取最长，长度相同再取字典序更小者（题面要求确定性输出）。
- 共 `2n-1` 个中心，每个最多扩 `n` 步；`n ≤ 1000` 时 O(n²) 足够。空串输出空行，单字符作为初始答案。
- 只比较当前扩展出的串，不必预存全部回文子串。
- 和区间 DP 比：额外空间常数、并列时直接比字典序，默写更短。

### 解法二：区间 DP

- `dp[i][j]` 表示 `s[i..j]` 是否回文：两端字符相等，且长度 ≤ 2 或 `dp[i+1][j-1]` 为真。
- 按区间长度递增填表，同时用当前区间更新「最长且字典序最小」的答案。
- 时间和中心扩展同阶，但要 O(n²) 布尔表；适合先把「子串回文」的递推写清楚，再改中心扩展。

### 解法三：Manacher

- 插入分隔符把奇偶中心统一，再利用已计算的回文半径关于对称中心加速。
- 时间 O(n)，实现与下标还原都明显重于本题数据范围。
- 并列字典序仍要还原原串再比较，不比中心扩展省事，竞赛模板题才值得上。

## 复杂度

- 解法一：时间 O(n²)，空间 O(1)（不计答案串）
- 解法二：时间 O(n²)，空间 O(n²)
- 解法三：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：2n-1 个中心扩展；更长优先，同长取字典序更小以保证输出确定。
import sys


def expand(s: str, l: int, r: int) -> str:
    # 从中心 (l,r) 向外扩到两边不等；奇数中心传 (i,i)，偶数传 (i,i+1)。
    n = len(s)
    while l >= 0 and r < n and s[l] == s[r]:
        l -= 1
        r += 1
    return s[l + 1 : r]  # 循环结束时 [l,r] 已越界或不等，合法区间是开区间内侧


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    if not s:
        print()  # 空串按约定输出空行
        return
    best = s[0]  # 单字符必回文，作为初始答案
    n = len(s)
    for i in range(n):
        for pal in (expand(s, i, i), expand(s, i, i + 1)):
            # 更长优先；同长取字典序更小，保证多解时输出确定。
            if len(pal) > len(best) or (len(pal) == len(best) and pal < best):
                best = pal
    print(best)


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：2n-1 个中心扩展；更长优先，同长取字典序更小以保证输出确定。
#include <bits/stdc++.h>
using namespace std;

string expand(const string& s, int l, int r) {
    // 从中心向外扩；结束后 [l,r] 已非法，合法子串是 (l, r)。
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
    if (!s.empty() && s.back() == '\r') s.pop_back();  // 兼容 CRLF
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
            // 更长优先；同长取字典序最小。
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
