## 思路

### 解法一（推荐）：左闭右开 lower_bound

- 要找的就是升序数组里第一个 `>= target` 的下标，也就是 `lower_bound`。
- 维护左闭右开区间 `[lo, hi)`：循环不变量是插入点一定落在这个区间内。
- `nums[mid] < target` 时答案在右侧，令 `lo = mid + 1`；否则 `mid` 仍可能是插入点，令 `hi = mid`。
- 结束时 `lo == hi`，这个位置就是插入点；若全部更小则落到 `n`。
- 元素即使有重复，该写法仍给出最左插入位。

### 解法二：闭区间二分

- 维护 `[lo, hi]`，循环条件 `lo <= hi`。
- `nums[mid] < target` 时 `lo = mid + 1`，`> target` 时 `hi = mid - 1`，相等可直接返回 `mid`。
- 循环结束时返回 `lo`（此时 `lo = hi + 1`，仍是第一个 `>= target` 的位置）。
- 与解法一差在区间开闭：闭区间遇到相等能提前返回，开区间把相等并进左半一起收缩。

### 解法三：线性扫描

- 从左扫到第一个 `>= target` 的下标，没有则返回 `n`。
- 正确但没用有序性，O(n)；用来对比「有序数组应走二分」。

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
    # 读入：n、升序数组、target（插入点可能是 n）
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    target = data[n + 1]
    # 左闭右开 [lo, hi)：插入点（第一个 >= target）始终落在此区间
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1  # mid 太小，答案在右侧
        else:
            hi = mid  # mid 仍可能是插入点，不能 mid-1
    # 结束时 lo == hi，全部更小则落到 n
    print(lo)


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
    // 读入：n、升序数组、target（插入点可能是 n）
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int target;
    cin >> target;
    // 左闭右开 [lo, hi)：第一个 >= target 的下标始终在此区间
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;  // mid 太小
        else hi = mid;                        // mid 仍可能是插入点
    }
    cout << lo << '\n';
    return 0;
}
```
