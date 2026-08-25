## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：回溯 DFS（推荐）

- 每位数字对应一段固定字母，组合就是在各位上做笛卡尔积，用 DFS/回溯逐位选字母。
- 映射表按 `abc`、`def` 这种字典序排好，按表顺序搜索，生成序列本身就是字典序；最后再 `sort` 一道更稳。
- 空串没有组合，直接不输出任何行（包括空行也不打）。
- 回溯用 path 追加/弹出，避免每层复制字符串。
- `1` 不在输入里，映射从 `2` 开始即可。

### 解法二：队列迭代积

- 从空串出发，每读一个数字就把当前队列里的串接上该键的每个字母，形成新一层。
- 本质是 BFS 层序做笛卡尔积，层数等于 digits 长度，结果集合与 DFS 相同。
- 空间要把一整层组合都摊在队列里，不如回溯的路径复用省。
- 空输入同样得到空结果，不要误输出空行。

## 复杂度

- 解法一：时间 O(4^m · m)，空间 O(m)（递归栈与路径；另需存放全部答案）
- 解法二：时间 O(4^m · m)，空间 O(4^m · m)（队列）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys

MAPPING = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def main():
    digits = sys.stdin.readline().rstrip("\n")
    if not digits:
        return
    ans = []

    def dfs(i, path):
        if i == len(digits):
            ans.append("".join(path))
            return
        for ch in MAPPING[digits[i]]:
            path.append(ch)
            dfs(i + 1, path)
            path.pop()

    dfs(0, [])
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

string mapping[10] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string digits;
    if (!(cin >> digits) || digits.empty()) return 0;
    vector<string> ans;
    string path;
    function<void(int)> dfs = [&](int i) {
        if (i == (int)digits.size()) {
            ans.push_back(path);
            return;
        }
        for (char ch : mapping[digits[i] - '0']) {
            path.push_back(ch);
            dfs(i + 1);
            path.pop_back();
        }
    };
    dfs(0);
    sort(ans.begin(), ans.end());
    for (const string& s : ans) cout << s << "\n";
    return 0;
}
```
