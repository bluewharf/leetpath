## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：滚动 DP（推荐）

- 线性 DP：走到第 i 间房，要么不偷它（继承前一间的最优），要么偷它（只能接前前间的最优 + 当前金额）。
- 转移就是 `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`，相邻约束被这一步吃掉。
- 最优解一定满足这个递推：若偷 i 就不能偷 i-1，否则就退化成不偷 i。
- 只用两个滚动变量，不必开数组。
- 从「前 0 间最优为 0」起步，单间房屋、全 0 金额都自然覆盖。

### 解法二：数组 DP / 记忆化

- 显式 `dp` 数组把每一间的最优都留下，便于对拍和讲转移；空间 O(n)。
- 自顶向下 `rob(i) = max(rob(i+1), nums[i] + rob(i+2))` 加备忘录，状态数同样线性。
- 与解法一完全等价，滚动只是把数组压成两个变量。
- 环状房屋（打家劫舍 II）时，数组 DP 更好改成「偷首不偷尾 / 反之」两段。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    print(prev1)


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
    int prev2 = 0, prev1 = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        int nxt = max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = nxt;
    }
    cout << prev1 << "\n";
    return 0;
}
```
