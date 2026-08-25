## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：排序作键（推荐）

- 字母异位词排序后完全相同，用排好序的串当哈希键，一次遍历即可分组。
- 组内按字典序排序；各组再按组内第一个串的字典序排序，输出顺序就确定了。
- 空串的键仍是空串，单独成组；该组输出一行空行。
- 必须按行读入，否则空字符串会被 `split()` 丢掉。
- n=0 时没有任何组，什么都不输出。

### 解法二：计数数组作键

- 只含小写字母时，用 26 维频次数组当键，每个串线性扫一遍就能入组。
- 单串从 O(k log k) 降到 O(k)，总时间 O(n k)；键序列化仍要 O(26)。
- 分组后的组内/组间排序与解法一相同，输出约定不变。
- 字符集一大（Unicode）就不如直接排序稳，所以模板仍用排序键。

## 复杂度

- 解法一：时间 O(n · k log k)（另加分组后 O(n log n) 排序），空间 O(n · k)
- 解法二：时间 O(n · k)，空间 O(n · k)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
