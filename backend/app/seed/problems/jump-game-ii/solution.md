## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：贪心分层（推荐）

- 求最少跳数，把数组看成按层扩展的 BFS：当前这一跳能覆盖的区间走完，才必须再跳一次。
- `cur_end` 是「当前跳跃次数」能到达的右边界；扫到边界就 `jumps++`，并把边界更新成这一层探到的最远 `far`。
- 只遍历到 `n - 2`：到达或越过终点时不必再跳，避免在终点处多计一次。
- 题目保证可达，所以不用处理走投无路；`n = 1` 时循环为空，答案 0。
- 贪心正确性：每一跳都把覆盖推到当前能及的最远，少一跳一定覆盖不到这个右端点。

### 解法二：DP 最少跳数

- `dp[i]` 表示跳到 i 的最少次数，对每个 i 枚举能到达它的 j 取 min。
- 朴素 O(n²)，小数据能过，但本题目标是线性。
- 用「上一跳的最远」把转移收成一层一层推进，就回到解法一，两者一脉相承。
- 现场先写贪心；被问正确性时再用 DP 定义解释。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n²)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    jumps = 0
    cur_end = 0
    far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = far
    print(jumps)


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
    int jumps = 0, cur_end = 0, far = 0;
    for (int i = 0; i < n - 1; i++) {
        far = max(far, i + nums[i]);
        if (i == cur_end) {
            jumps++;
            cur_end = far;
        }
    }
    cout << jumps << "\n";
    return 0;
}
```
