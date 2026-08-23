## 思路

- 字母异位词排序后完全相同，用排好序的串当哈希键，一次遍历即可分组。
- 组内按字典序排序；各组再按组内第一个串的字典序排序，输出顺序就确定了。
- 空串的键仍是空串，单独成组；该组输出一行空行。
- 必须按行读入，否则空字符串会被 `split()` 丢掉。
- n=0 时没有任何组，什么都不输出。

## 复杂度

- 时间：O(n · k log k)，k 为单个字符串最大长度（排序作键）；分组后的排序不超过 O(n log n)
- 空间：O(n · k)

## 模板代码

### Python3

```python
import sys
from collections import defaultdict


def main():
    data = sys.stdin.read()
    lines = data.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    n = int(lines[0])
    strs = lines[1 : 1 + n]
    while len(strs) < n:
        strs.append("")
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    result = []
    for g in groups.values():
        g.sort()
        result.append(g)
    result.sort(key=lambda g: g[0])
    for g in result:
        print(" ".join(g))


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
    string line;
    if (!getline(cin, line)) return 0;
    int n = stoi(line);
    vector<string> strs(n);
    for (int i = 0; i < n; i++) {
        if (!getline(cin, strs[i])) strs[i] = "";
    }
    unordered_map<string, vector<string>> groups;
    for (const string& s : strs) {
        string key = s;
        sort(key.begin(), key.end());
        groups[key].push_back(s);
    }
    vector<vector<string>> result;
    result.reserve(groups.size());
    for (auto& kv : groups) {
        sort(kv.second.begin(), kv.second.end());
        result.push_back(kv.second);
    }
    sort(result.begin(), result.end(),
         [](const vector<string>& a, const vector<string>& b) {
             return a[0] < b[0];
         });
    for (const auto& g : result) {
        for (size_t i = 0; i < g.size(); i++) {
            if (i) cout << " ";
            cout << g[i];
        }
        cout << "\n";
    }
    return 0;
}
```
