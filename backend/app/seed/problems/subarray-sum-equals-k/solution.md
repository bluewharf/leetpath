## 思路

### 解法一（推荐）：前缀和 + 哈希计数

- 连续子数组和转前缀和：`sum(l..r) = pre[r] - pre[l-1]`，于是要找有多少个 `pre[j] == pre[i] - k`（`j < i`）。
- 边扫边用哈希表统计「某个前缀和出现过多少次」，查 `s - k` 的出现次数累加到答案。
- 先查询再把当前 `s` 计入表，避免把「自己减自己」当成一个空区间。
- 初始 `cnt[0] = 1`，对应空前缀，这样从下标 0 出发、和恰好为 `k` 的前缀也能算上。
- 数组含负数，滑动窗口单调性不成立，必须用哈希而不能用双指针。

### 解法二：前缀和数组 + 枚举两端

- 先 O(n) 算出 `pre[0..n]`，再枚举右端 `i`、左端 `j < i`，若 `pre[i] - pre[j] == k` 则计数。
- 不变量仍是前缀差，但不做哈希，时间掉到 O(n²)。
- 与解法一差在：用双重循环换掉「补数出现次数」的 O(1) 查询，n 稍大即超时。

### 解法三：暴力枚举每个子数组

- 枚举左端、右端，内层再累加，或右端延伸时滚动和。
- 滚动和可压到 O(n²)，三层累加是 O(n³)；都不利用前缀结构，只作正确性对照。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n²)，空间 O(n)
- 解法三：时间 O(n²)（滚动和）或 O(n³)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import defaultdict


def main() -> None:
    # 读入：n、数组、目标和 k（数组可含负数，不能滑窗）
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    k = int(data[n + 1])
    # cnt[pre] = 该前缀和出现次数；sum(l..r)=k ⇔ 存在 j<i 使 pre[j]=pre[i]-k
    cnt = defaultdict(int)
    cnt[0] = 1  # 空前缀：从下标 0 起和恰好为 k 的那段也要算
    s = 0
    ans = 0
    for x in nums:
        s += x
        ans += cnt[s - k]  # 先查再写入，避免空区间「自己减自己」
        cnt[s] += 1
    print(ans)


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
    // 读入：n、数组、k（含负数，不能靠滑窗单调性）
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int k;
    cin >> k;
    // cnt[pre]：该前缀和出现次数；先查 s-k 再写入当前 s
    unordered_map<int, int> cnt;
    cnt[0] = 1;  // 空前缀，覆盖从下标 0 开始的子数组
    int s = 0;
    long long ans = 0;
    for (int x : nums) {
        s += x;
        auto it = cnt.find(s - k);
        if (it != cnt.end()) ans += it->second;
        cnt[s]++;
    }
    cout << ans << '\n';
    return 0;
}
```
