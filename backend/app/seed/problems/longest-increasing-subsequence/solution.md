## 思路

### 解法一：贪心 + 二分 tails（推荐）

- 维护 `tails[k]`：所有长度为 `k+1` 的严格递增子序列里，最小的可能结尾。
- `tails` 本身严格递增；对新来的 `x` 用 `bisect_left` / `lower_bound` 找第一个 `>= x` 的位置替换（严格递增不能用 `upper_bound`）。
- 替换不增加长度，只让「同样长」的结尾更小，给后面更大的数留下增长空间；`x` 比所有结尾都大则追加。
- `tails` 的长度等于 LIS 长度，它本身不一定是某条真实子序列——这是和「直接记 dp 序列」最大的差别。
- 和 O(n²) DP 比：用「更小的结尾更好」把内层扫描换成二分。

### 解法二：一维 DP

- `dp[i]` 表示以 `nums[i]` 结尾的 LIS 长度，转移 `dp[i] = max{dp[j]} + 1`（`j < i` 且 `nums[j] < nums[i]`），没有更小的 j 则为 1。
- 答案是所有 `dp[i]` 的最大值；顺手记 `pred[i]` 就能还原一条具体序列。
- 时间 O(n²)，n 到 2500 仍可过，先写对再优化时用这套最贴定义。

### 解法三：树状数组优化 DP

- 把值离散化后，按「结尾值」在树状数组里维护最大 `dp`：查询严格小于 `x` 的前缀 max，再单点更新。
- 时间同样 O(n log n)，能同时拿到长度和方案，结构比 tails 重。
- 只求长度时解法一更短；值域查询、带约束的 LIS 变体才值得上这套。

## 复杂度

- 解法一：时间 O(n log n)，空间 O(n)
- 解法二：时间 O(n²)，空间 O(n)
- 解法三：时间 O(n log n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import bisect
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    tails: list[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    print(len(tails))


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
    vector<int> tails;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    cout << (int)tails.size() << "\n";
    return 0;
}
```
