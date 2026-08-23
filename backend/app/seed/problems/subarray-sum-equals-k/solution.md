## 思路

- 连续子数组和转前缀和：`sum(l..r) = pre[r] - pre[l-1]`，于是要找有多少个 `pre[j] == pre[i] - k`（`j < i`）。
- 边扫边用哈希表统计「某个前缀和出现过多少次」，查 `s - k` 的出现次数累加到答案。
- 先查询再把当前 `s` 计入表，避免把「自己减自己」当成一个空区间。
- 初始 `cnt[0] = 1`，对应空前缀，这样从下标 0 出发、和恰好为 `k` 的前缀也能算上。
- 数组含负数，滑动窗口单调性不成立，必须用哈希而不能用双指针。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys
from collections import defaultdict


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    k = int(data[n + 1])
    cnt = defaultdict(int)
    cnt[0] = 1
    s = 0
    ans = 0
    for x in nums:
        s += x
        ans += cnt[s - k]
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
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int k;
    cin >> k;
    unordered_map<int, int> cnt;
    cnt[0] = 1;
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
