## 思路

- 每位数字对应一段固定字母，组合就是在各位上做笛卡尔积，用 DFS/回溯逐位选字母。
- 映射表按 `abc`、`def` 这种字典序排好，按表顺序搜索，生成序列本身就是字典序；最后再 `sort` 一道更稳。
- 空串没有组合，直接不输出任何行（包括空行也不打）。
- 回溯用 path 追加/弹出，避免每层复制字符串。
- `1` 不在输入里，映射从 `2` 开始即可。

## 复杂度

- 时间：O(4^m · m)，m 为数字个数
- 空间：O(m)（递归栈与路径）

## 模板代码

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
