## 思路

### 解法一（推荐）：有序半边二分

- 旋转后的升序数组仍能二分：`mid` 把区间切成两段，其中一段一定有序。
- 用 `nums[lo] <= nums[mid]` 判断左半是否有序；否则右半有序。
- 有序那一侧像普通二分一样判断 `target` 是否落在闭开区间内，落在则收缩到这一侧，否则丢掉这一侧。
- 元素互不相同，比较不会卡在相等边界上，每次都能严格丢掉一半。
- 找不到时返回 `-1`；未旋转（断点在 `0`）时全程左半有序，退化为普通二分。

### 解法二：先找断点再普通二分

- 先二分找最小值下标 `pivot`（与「寻找旋转排序数组中的最小值」同一套比较）。
- 再根据 `target` 与 `nums[0]` 的大小，把查找限制在 `[0, pivot)` 或 `[pivot, n)` 上做普通二分。
- 两次独立的二分，模块更清晰，但常数比解法一「每步现场判断哪半有序」更大。
- 未旋转时 `pivot = 0`，第二段就是整段数组，同样正确。

### 解法三：线性扫描

- 从左到右比较，相等即返回下标，否则 `-1`。
- 不利用有序和旋转结构，时间掉到 O(n)，面试里用来对比「为什么必须二分」。
- 仅当 n 极小或无法保证有序时才合理。

## 复杂度

- 解法一：时间 O(log n)，空间 O(1)
- 解法二：时间 O(log n)，空间 O(1)
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    target = data[n + 1]
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            print(mid)
            return
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    print(-1)


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
    int target;
    cin >> target;
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            cout << mid << '\n';
            return 0;
        }
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    cout << -1 << '\n';
    return 0;
}
```
