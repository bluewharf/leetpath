## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：回溯剪枝（推荐）

- 回溯生成长度为 2n 的括号串：任何前缀里左括号不少于右括号，且左右各正好 n 个。
- 还能放左括号（已放左 < n）就放；还能放右括号（已放右 < 已放左）就放。这两个条件同时保证合法。
- 先尝试 `'('` 再尝试 `')'`，搜索顺序本身接近字典序；生成后再 sort 一次，输出完全确定。
- 非法前缀被剪掉，不会爆搜到无效分支。
- 合法串数量是第 n 个卡特兰数，n ≤ 8 可以直接枚举。

### 解法二：卡特兰递推 DP

- 合法串一定是 `( A ) B`，A、B 为更短的合法串。枚举左块长度，笛卡尔积拼接。
- 自底向上从 0 算到 n，得到全部 C_n 个串，集合与回溯相同。
- 要把所有中间长度的串都存下来，输出前仍需排序以满足字典序。
- 现场写回溯更短；DP 用来解释「为什么数量是卡特兰数」。

## 复杂度

- 解法一：时间 O(C_n · n)，空间 O(n) 递归栈（另需 O(C_n · n) 存放全部答案）
- 解法二：时间 O(C_n · n)，空间 O(C_n · n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    n = int(sys.stdin.read().strip())
    ans = []

    def dfs(cur, open_cnt, close_cnt):
        if len(cur) == 2 * n:
            ans.append("".join(cur))
            return
        if open_cnt < n:
            cur.append("(")
            dfs(cur, open_cnt + 1, close_cnt)
            cur.pop()
        if close_cnt < open_cnt:
            cur.append(")")
            dfs(cur, open_cnt, close_cnt + 1)
            cur.pop()

    dfs([], 0, 0)
    ans.sort()
    for s in ans:
        print(s)


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
    int n;
    cin >> n;
    vector<string> ans;
    string cur;
    function<void(int, int)> dfs = [&](int open_cnt, int close_cnt) {
        if ((int)cur.size() == 2 * n) {
            ans.push_back(cur);
            return;
        }
        if (open_cnt < n) {
            cur.push_back('(');
            dfs(open_cnt + 1, close_cnt);
            cur.pop_back();
        }
        if (close_cnt < open_cnt) {
            cur.push_back(')');
            dfs(open_cnt, close_cnt + 1);
            cur.pop_back();
        }
    };
    dfs(0, 0);
    sort(ans.begin(), ans.end());
    for (const string& s : ans) cout << s << "\n";
    return 0;
}
```
