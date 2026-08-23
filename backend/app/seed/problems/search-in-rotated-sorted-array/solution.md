## 思路

- 旋转后的升序数组仍能二分：`mid` 把区间切成两段，其中一段一定是有序的。
- 用 `nums[lo] <= nums[mid]` 判断左半是否有序；否则右半有序。
- 有序那一侧像普通二分一样判断 `target` 是否落在闭开区间内，落在则收缩到这一侧，否则丢弃这一侧。
- 元素互不相同，比较不会卡在相等边界上，每次都能严格丢掉一半。
- 找不到时返回 `-1`；未旋转（断点在 `0`）时全程左半有序，退化为普通二分。

## 复杂度

- 时间：O(log n)
- 空间：O(1)

## 模板代码

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
