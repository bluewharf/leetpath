## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：与右端比较的二分（推荐）

- 旋转后的数组是两段升序拼接，最小元就是断点（右半段的第一个数）。
- 用 `nums[mid]` 和右端 `nums[hi]` 比较就能判断 mid 落在哪一段：比 hi 大，说明还在左半段，断点在右侧。
- 否则 mid 已经在右半段（或整个数组未真正错位），断点在 `[lo, mid]`。
- 元素互不相同，不会出现 `nums[mid] == nums[hi]` 无法收缩的情况。
- 循环不变量：最小值始终在闭区间 `[lo, hi]` 里，直到 `lo == hi`。

### 解法二：线性扫一遍

- 从左到右找第一个下降点 `nums[i] < nums[i-1]`，该处就是最小值；若全程递增则答案是 `nums[0]`。
- 写起来零负担，但浪费了「有序 + 旋转」的结构，面试会被追问如何压到对数。
- 与左端比较的二分也成立，但未旋转时要特判 `nums[lo] < nums[hi]`，边界比盯住右端烦。

## 复杂度

- 解法一：时间 O(log n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    print(nums[lo])


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
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    cout << nums[lo] << "\n";
    return 0;
}
```
