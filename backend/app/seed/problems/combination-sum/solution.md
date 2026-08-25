## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：排序回溯（可重复选）（推荐）
- 先排序再回溯：每一层从 `start` 往后选，路径里的数非递减，组合自动去重。
- 同一个数可以重复选，递归时下标仍传 `i` 而不是 `i+1`。
- `candidates[i] > remain` 时后面更大，直接 `break` 剪枝；`remain == 0` 收进答案。
- 元素互异 + 有序选取，不会出现同一多重集的不同排列。
- 收集后按字典序输出（从小到大选时通常已经有序）。模板即此写法。

### 解法二：完全背包 DP 收集组合
- `dp[x]` 存所有和为 `x` 的组合；外层循环硬币、内层金额从小到大，保证每种组合只按一种顺序生成。
- 与解法一枚举的集合相同，但要把每个状态的全部路径都存下来，空间随方案数膨胀。
- 时间仍是指数级（方案数本身可能很多），实现比回溯笨重，剪枝也不如 `break` 直观。
- 更适合「只问方案数」的变体；本题要输出全部组合，面试默认回溯。

## 复杂度

- 解法一：时间 O(n^{T/m}) 量级（T 为目标，m 为最小面额），空间 O(T/m)（递归深度与路径）
- 解法二：时间 O(n · T · 方案数)，空间 O(T · 方案数)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    candidates = list(map(int, data[1 : 1 + n]))
    target = int(data[1 + n])
    candidates.sort()
    res = []

    def dfs(start, remain, path):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, n):
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            dfs(i, remain - c, path)
            path.pop()

    dfs(0, target, [])
    res.sort()
    for comb in res:
        print(" ".join(map(str, comb)))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

void dfs(int start, int remain, vector<int>& path, const vector<int>& cand,
         vector<vector<int>>& res) {
    if (remain == 0) {
        res.push_back(path);
        return;
    }
    int n = (int)cand.size();
    for (int i = start; i < n; ++i) {
        if (cand[i] > remain) break;
        path.push_back(cand[i]);
        dfs(i, remain - cand[i], path, cand, res);
        path.pop_back();
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> candidates(n);
    for (int i = 0; i < n; ++i) cin >> candidates[i];
    int target;
    cin >> target;
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> res;
    vector<int> path;
    dfs(0, target, path, candidates, res);
    sort(res.begin(), res.end());
    for (const auto& comb : res) {
        for (size_t i = 0; i < comb.size(); ++i) {
            if (i) cout << ' ';
            cout << comb[i];
        }
        cout << '\n';
    }
    return 0;
}
```
