## 思路

- 回溯生成长度为 2n 的括号串：任何前缀里左括号不少于右括号，且左右各正好 n 个。
- 还能放左括号（已放左 < n）就放；还能放右括号（已放右 < 已放左）就放。这两个条件同时保证合法。
- 先尝试 `'('` 再尝试 `')'`，搜索顺序本身接近字典序；生成后再 sort 一次，输出完全确定。
- 非法前缀被剪掉，不会爆搜到无效分支。
- 合法串数量是第 n 个卡特兰数，n ≤ 8 可以直接枚举。

## 复杂度

- 时间：O(C_n · n)，C_n 为第 n 个卡特兰数（约 4^n / n^{3/2}）
- 空间：O(n) 递归栈（另需 O(C_n · n) 存放全部答案）

## 模板代码

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
