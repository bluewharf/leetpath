## 思路

- 要的是降序第 k 个，不是第 k 个不同值，重复元素都要占名次。
- 维护一个大小为 k 的小根堆：堆顶始终是「目前这 k 个大数里最小的那个」。
- 新来的数比堆顶大就换进去，堆里始终是全局最大的 k 个；扫完堆顶即第 k 大。
- 比全排序更贴面试口径，k 远小于 n 时额外空间也更小。
- 不必去重，相同值多次入堆即可。

## 复杂度

- 时间：O(n log k)
- 空间：O(k)

## 模板代码

### Python3

```python
import heapq
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    print(h[0])


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
    priority_queue<int, vector<int>, greater<int>> h;
    for (int x : nums) {
        h.push(x);
        if ((int)h.size() > k) h.pop();
    }
    cout << h.top() << "\n";
    return 0;
}
```
