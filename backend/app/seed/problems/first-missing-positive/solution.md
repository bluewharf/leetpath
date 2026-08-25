## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：原地交换归位（推荐）

- 缺失的最小正整数只可能是 `1..n+1`：出现过的正数最多把 `1..n` 全部填满。
- 把数组本身当哈希表：值为 x∈[1,n] 的数应放到下标 x-1。
- 用交换把每个合法 x 归位；若目标槽已经是 x，立刻停，避免重复值死循环。
- 负数、0、大于 n 的数都是垃圾，占着槽位也没关系，它们不会被当成「已归位」。
- 再扫一遍，第一个 `nums[i] != i+1` 的位置就是答案；若全对，缺的是 n+1。

### 解法二：哈希集合

- 把所有正数丢进集合，从 1 往上查第一个不在集合里的数。
- 思路直白，时间和空间都是 O(n)，过不了「常数额外空间」的约束。
- 面试可先口述这个，再说明「数组下标就是哈希」，过渡到解法一。

### 解法三：排序后扫描

- 原地排序后从 1 起扫过所有正数，遇到缺口就返回；全是更大的正数则答案是 1。
- 负数和 0 都跳过，碰到第一个大于「当前期望正数」的位置就是缺口。
- 时间 O(n log n)，同样改了原数组，没有用上「答案不超过 n+1」这一关键。

## 复杂度

- 解法一：时间 O(n)，空间 O(1) 额外（就地交换）
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n log n)，空间 O(1) 额外（原地排序）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0]) if data else 0
    nums = list(map(int, data[1 : 1 + n]))
    # 把 x∈[1,n] 交换到下标 x-1；目标槽已是 x 则停，避免重复值死循环
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    # 第一个没归位的下标 i 对应缺失 i+1；全对则缺 n+1
    for i in range(n):
        if nums[i] != i + 1:
            print(i + 1)
            return
    print(n + 1)


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
    // 把 x∈[1,n] 交换到下标 x-1；目标槽已是 x 则停，避免重复值死循环
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int j = nums[i] - 1;
            swap(nums[i], nums[j]);
        }
    }
    // 第一个没归位的下标 i 对应缺失 i+1；全对则缺 n+1
    for (int i = 0; i < n; i++) {
        if (nums[i] != i + 1) {
            cout << i + 1 << "\n";
            return 0;
        }
    }
    cout << n + 1 << "\n";
    return 0;
}
```
