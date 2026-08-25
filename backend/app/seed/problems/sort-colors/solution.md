## 思路

### 解法一（推荐）：荷兰国旗三指针

- 三路快排 / 荷兰国旗：一次扫描把 `0` 丢到左边、`2` 丢到右边，中间自然是 `1`。
- 三个指针：`lo` 是下一个 `0` 应放的位置，`hi` 是下一个 `2` 应放的位置，`i` 扫描未知区。
- 遇到 `0`：与 `lo` 交换后 `lo++`、`i++`（换过来的只可能是 `0` 或 `1`，已处理过）。
- 遇到 `2`：与 `hi` 交换后只 `hi--`，`i` 不动，因为从右边换来的值还没看过。
- 遇到 `1`：直接 `i++`。循环条件是 `i <= hi`，未知区空了就结束。

### 解法二：计数后两遍写回

- 先数 `0/1/2` 各有多少，再按个数依次覆盖原数组。
- 不变量是「颜色只有三种」，稳定、不容易写错指针。
- 与解法一差在扫两遍、且必须知道值域极小；解法一是一趟原地交换，更贴近「常数空间、一次划分」。

### 解法三：普通排序

- 直接对数组排序。值域虽小，比较排序仍是 O(n log n)，没有用上「只有 0/1/2」。
- 面试保底，不是这题想考的原地三路划分。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n log n)，空间 O(1) 或 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    # 读入：n 与只含 0/1/2 的数组
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    # 荷兰国旗：[0,lo) 全 0，[lo,i) 全 1，(hi,n) 全 2，[i,hi] 未知
    lo, i, hi = 0, 0, n - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1  # 从左边换来的只可能是 0/1，已处理过
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1  # 从右边换来的还没看过，i 不动
        else:
            i += 1
    print(*nums)


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
    // 读入：n 与只含 0/1/2 的数组
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    // 荷兰国旗：[0,lo) 全 0，[lo,i) 全 1，(hi,n) 全 2，[i,hi] 未知
    int lo = 0, i = 0, hi = n - 1;
    while (i <= hi) {
        if (nums[i] == 0) {
            swap(nums[lo], nums[i]);
            lo++;
            i++;  // 左边换来的已处理过
        } else if (nums[i] == 2) {
            swap(nums[i], nums[hi]);
            hi--;  // 右边换来的未看过，i 不动
        } else {
            i++;
        }
    }
    for (int j = 0; j < n; j++) {
        if (j) cout << ' ';
        cout << nums[j];
    }
    cout << '\n';
    return 0;
}
```
