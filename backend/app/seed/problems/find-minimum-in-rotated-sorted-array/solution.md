## 思路

- 旋转后的数组是两段升序拼接，最小元就是断点（右半段的第一个数）。
- 用 `nums[mid]` 和右端 `nums[hi]` 比较就能判断 mid 落在哪一段：比 hi 大，说明还在左半段，断点在右侧。
- 否则 mid 已经在右半段（或整个数组未真正错位），断点在 `[lo, mid]`。
- 元素互不相同，不会出现 `nums[mid] == nums[hi]` 无法收缩的情况。
- 循环不变量：最小值始终在闭区间 `[lo, hi]` 里，直到 `lo == hi`。

## 复杂度

- 时间：O(log n)
- 空间：O(1)

## 模板代码

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
