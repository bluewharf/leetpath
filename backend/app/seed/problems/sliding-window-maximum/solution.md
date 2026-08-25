## 思路

### 解法一（推荐）：单调递减队列

- 维护一个下标单调队列，队头始终是当前窗口的最大值下标。
- 队列里的值从队头到队尾严格递减：新来的 `x` 把所有 `<= x` 的尾部弹掉，它们不可能再当最大值。
- 队头下标一旦滑出窗口左边界（`<= i - k`）就弹出。
- 当下标 `i >= k - 1` 时窗口成形，`nums[dq[0]]` 就是该窗口答案。
- 每个下标最多入队、出队一次，整体线性。

### 解法二：大根堆 + 过期下标

- 堆里存 `(值, 下标)`，窗口右端每进一步就入堆。
- 堆顶下标 `<= i - k` 时视为过期，不断弹出，直到堆顶落在窗口内。
- 不变量是「堆顶是尚未过期的最大元素」，但堆里会残留过期项，空间可能到 O(n)。
- 与解法一差在：堆不能在入堆时清掉「被新值盖住」的旧值，只能懒删除。

### 解法三：每个窗口扫一遍

- 对每个左端点 `i`，在 `[i, i+k)` 里取 max。
- 正确但时间 O(nk)，窗口之间没有复用信息，用来反衬单调队列的线性。

## 复杂度

- 解法一：时间 O(n)，空间 O(k)
- 解法二：时间 O(n log n)，空间 O(n)
- 解法三：时间 O(nk)，空间 O(1)（不计答案）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import deque


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    dq = deque()
    ans = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            ans.append(nums[dq[0]])
    print(" ".join(map(str, ans)))


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
    int k;
    cin >> k;
    deque<int> dq;
    vector<int> ans;
    for (int i = 0; i < n; i++) {
        while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) ans.push_back(nums[dq.front()]);
    }
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```
