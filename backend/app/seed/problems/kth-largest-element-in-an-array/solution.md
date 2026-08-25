## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：大小为 k 的小根堆（推荐）

- 要的是降序第 k 个，不是第 k 个不同值，重复元素都要占名次。
- 维护一个大小为 k 的小根堆：堆顶始终是「目前这 k 个大数里最小的那个」。
- 新来的数入堆，超过 k 个就弹出堆顶，堆里始终是全局最大的 k 个；扫完堆顶即第 k 大。
- 比全排序更贴面试口径，k 远小于 n 时额外空间也更小。
- 不必去重，相同值多次入堆即可。

### 解法二：快速选择

- 按快排切分，枢轴最终下标就是它的名次；目标是升序第 n-k 位。
- 只递归枢轴的一侧，平均 O(n)，最坏 O(n²)（随机枢轴可摊平）。
- 原地改数组，额外空间 O(1)；面试常作为堆的后续追问。
- 与堆相比期望更快，但最坏情况和「会打乱输入」要讲清楚。

### 解法三：全排序

- 排序后取倒数第 k 个，O(n log n)，实现零风险。
- 升序取 `nums[n-k]`，降序取 `nums[k-1]`，不要和第 k 个不同值搞混。
- k 接近 n 时与堆同阶；本题考的是堆/选择，排序只能当保底。

## 复杂度

- 解法一：时间 O(n log k)，空间 O(k)
- 解法二：时间平均 O(n)、最坏 O(n²)，空间 O(1)
- 解法三：时间 O(n log n)，空间 O(1) 额外（原地排序）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
