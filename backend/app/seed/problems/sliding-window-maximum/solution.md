## 思路

- 维护一个下标单调队列，队头始终是当前窗口的最大值下标。
- 队列里的值从队头到队尾严格递减：新来的 `x` 把所有 `<= x` 的尾部弹掉，它们不可能再当最大值。
- 队头下标一旦滑出窗口左边界（`<= i - k`）就弹出。
- 当下标 `i >= k - 1` 时窗口成形，`nums[dq[0]]` 就是该窗口答案。
- 每个下标最多入队、出队一次，整体线性。

## 复杂度

- 时间：O(n)
- 空间：O(k)

## 模板代码

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
