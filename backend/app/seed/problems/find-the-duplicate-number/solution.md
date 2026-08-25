## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：Floyd 判圈（推荐）

- 值域 `[1, n]`、长度 `n+1`，把下标 i 看成指向 `nums[i]` 的指针，数组就是一张有环的函数图。
- 重复值意味着有两个入口指向同一个节点，环的入口就是那个重复数。
- Floyd：快慢指针先相遇证明有环，再把慢指针拉回起点同步走，第二次相遇必在环入口。
- 值从 1 开始，0 不会被任何节点指向，从 `nums[0]` 出发一定能进环。
- 全程只读两个指针，满足「不改数组 + O(1) 额外空间」。

### 解法二：值域二分计数

- 答案落在 `[1, n]`。取 mid，统计 `<= mid` 的个数：超过 mid 则重复值在左半，否则在右半。
- 抽屉原理保证重复数所在一侧计数会「超员」，每次丢掉一半值域。
- 不改数组、额外空间 O(1)，但时间多一个 log，是 Floyd 的常见对照解。
- 二分的是值不是下标，不要写成普通数组二分。

### 解法三：哈希 / 排序

- 哈希集合边扫边查，第一次撞见的就是重复数，O(n) 时间但 O(n) 空间，题目通常不允许。
- 排序后找相邻相等，破坏原数组，也不满足原地只读。
- 用来对照约束：本题考点就是空间 O(1) 且不改输入。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n log n)，空间 O(1)
- 解法三：时间 O(n)（哈希）或 O(n log n)（排序），空间 O(n) 或 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    print(slow)


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
    int slow = nums[0], fast = nums[0];
    while (true) {
        slow = nums[slow];
        fast = nums[nums[fast]];
        if (slow == fast) break;
    }
    slow = nums[0];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    cout << slow << "\n";
    return 0;
}
```
