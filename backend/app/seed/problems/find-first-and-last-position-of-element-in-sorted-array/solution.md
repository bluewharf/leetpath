## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：两次 lower_bound（推荐）

- 有序数组上求目标值的闭区间，本质是两次「找下界」二分，整体 O(log n)。
- 第一次找第一个 `>= target` 的下标 L：越界或 `nums[L] != target` 说明根本没有这个数。
- 第二次找第一个 `>= target+1` 的下标，再减一，就是最后一个 target。
- 把「最后一个等于」改写成「第一个大于的前驱」，两套二分边界完全一样，不容易写错。
- 空数组时 L 会落到 n，与「找不到」走同一条失败分支。

### 解法二：左右端点分别二分

- 找左端：`nums[mid] >= target` 时收右，否则扩左，停在第一个等于 target 的位置。
- 找右端：`nums[mid] <= target` 时扩左，否则收右，停在最后一个等于 target 的位置。
- 两套比较符号刚好相反，`lo/hi` 闭开区间容易写反，不如统一成 lower_bound。
- 找不到时同样输出 `-1 -1`；与解法一复杂度相同，只是边界写法不同。

## 复杂度

- 解法一：时间 O(log n)，空间 O(1)
- 解法二：时间 O(log n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    target = data[1 + n]
    left = lower_bound(nums, target)
    if left == n or nums[left] != target:
        print(-1, -1)
        return
    right = lower_bound(nums, target + 1) - 1
    print(left, right)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int lower_bound_idx(const vector<int>& a, int x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int target;
    cin >> target;
    int left = lower_bound_idx(nums, target);
    if (left == n || nums[left] != target) {
        cout << -1 << " " << -1 << "\n";
        return 0;
    }
    int right = lower_bound_idx(nums, target + 1) - 1;
    cout << left << " " << right << "\n";
    return 0;
}
```
