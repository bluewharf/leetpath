## 思路

### 解法一（推荐）：二进制枚举

- 元素互不相同，幂集可以用 `0 .. 2^n-1` 的二进制枚举：第 `i` 位为 1 表示选 `nums[i]`。
- 每个掩码对应一个子集，子集内部先排序，保证行内升序。
- 全部子集再按 `(长度, 序列字典序)` 排序，空集长度 0 一定排在最前，对应一个空行。
- `n <= 10`，`2^n` 最多 1024，枚举加排序完全可接受。
- 不要用哈希去重：输入无重复，排序后的输出规则已经唯一确定。

### 解法二：回溯选 / 不选

- 对下标 `i` 两条分支：把 `nums[i]` 放进路径，或不放，递归到 `i+1`；到底把当前路径拷进答案。
- 若按下标顺序做选择，路径本身已是原数组顺序，再对路径排序即可满足行内升序。
- 与解法一差在：用递归树展开「每个元素选或不选」，而不是把选择压成一个整数掩码；便于改成「有重复元素的子集」题。

### 解法三：迭代扩展

- 从只含空集开始，每读入一个数，把已有每个子集复制一份并追加该数。
- 不变量：处理完前 i 个数，列表里正好是这 i 个数的幂集。
- 与前两种等价，只是按「新元素 × 旧子集」增量构造，没有显式掩码或递归栈。

## 复杂度

- 解法一：时间 O(n · 2^n + 2^n log 2^n)，空间 O(n · 2^n)
- 解法二：时间 O(n · 2^n + 2^n log 2^n)，空间 O(n · 2^n)（含递归深度 O(n)）
- 解法三：时间 O(n · 2^n + 2^n log 2^n)，空间 O(n · 2^n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    subsets = []
    for mask in range(1 << n):
        cur = [nums[i] for i in range(n) if mask & (1 << i)]
        cur.sort()
        subsets.append(cur)
    subsets.sort(key=lambda s: (len(s), s))
    for s in subsets:
        if s:
            print(*s)
        else:
            print()


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
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    vector<vector<int>> subsets;
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> cur;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i)) cur.push_back(nums[i]);
        sort(cur.begin(), cur.end());
        subsets.push_back(cur);
    }
    sort(subsets.begin(), subsets.end(), [](const vector<int>& a, const vector<int>& b) {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;
    });
    for (const auto& s : subsets) {
        for (size_t i = 0; i < s.size(); i++) {
            if (i) cout << ' ';
            cout << s[i];
        }
        cout << '\n';
    }
    return 0;
}
```
