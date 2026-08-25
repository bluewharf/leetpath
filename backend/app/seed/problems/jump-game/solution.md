## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：贪心最远可达（推荐）

- 贪心维护「从起点出发目前能摸到的最远下标 `far`」，不必搜索所有跳法。
- 扫描到 i 时若 `i > far`，说明前面所有可达位置都跳不过来，后面更到不了，直接判失败。
- 否则用 `i + nums[i]` 刷新 `far`：当前位置能跳到的更远处，成为新的可达上界。
- 不变量：循环进行到 i 时，`[0, far]` 都可达；能扫完全程则终点必在这个区间里。
- `n = 1` 已经站在终点，无论 `nums[0]` 是不是 0 都成功。

### 解法二：从后往前标记

- 从终点往左推「最左可达位置」：若 `i + nums[i]` 能摸到当前目标，就把目标改成 i。
- 扫完后目标落到 0 则成功。本质也是贪心，只是不变量改成「目标右侧（含）都能到终点」。
- 也可以 `dp[i]` 表示 i 是否可达，从左刷每个跳跃，最坏接近平方。
- 面试要的是线性贪心；DP 只用来说明最优子结构。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)（从后往前）或 O(n²)（朴素 DP），空间 O(1) 或 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    # far 是目前能摸到的最远下标；不变量：[0, far] 都可达
    far = 0
    for i in range(n):
        if i > far:
            print("false")
            return
        far = max(far, i + nums[i])
    print("true")


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
    // far 是目前能摸到的最远下标；不变量：[0, far] 都可达
    int far = 0;
    for (int i = 0; i < n; i++) {
        if (i > far) {
            cout << "false\n";
            return 0;
        }
        far = max(far, i + nums[i]);
    }
    cout << "true\n";
    return 0;
}
```
