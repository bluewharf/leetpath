## 思路

### 解法一（推荐）：0-1 背包可行性 DP

- 能拆成两个等和子集，当且仅当存在一个子集和恰好等于 `total / 2`；总和为奇数时直接不可能。
- 转化成 0-1 背包的可行性问题：`dp[s]` 表示能否凑出和 `s`。
- 每个数 `x` 倒序更新 `dp[s] |= dp[s - x]`，倒序是为了保证每个数只用一次。
- `dp[0] = true` 作起点；一旦 `dp[target]` 变为真就可以提前结束。

### 解法二：bitset 滚动

- 用二进制位表示可达和：每加入 `x` 做 `bits |= bits << x`，与一维 DP 同一不变量。
- 按机器字长并行，常数更好；C++ `bitset` 或手写 64 位数组都能写。
- 仍是「每个数用一次」，只是状态从布尔数组换成位图。

### 解法三：记忆化搜索

- `dfs(i, rest)`：考虑 `nums[i:]` 能否凑出 `rest`；`rest == 0` 成功，越界或为负失败。
- 状态 O(n · target)，与 DP 同阶，但递归常数和栈开销更大。
- 适合从「选或不选」讲起，再压缩成解法一的倒序滚动数组。

## 复杂度

- 解法一：时间 O(n · target)，空间 O(target)，其中 `target = sum(nums) / 2`
- 解法二：时间 O(n · target / w)，空间 O(target / w)，`w` 为字长
- 解法三：时间 O(n · target)，空间 O(n · target)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    total = sum(nums)
    if total % 2 != 0:  # 总和为奇，不可能均分
        print("false")
        return
    target = total // 2
    # 不变量：dp[s] 表示能否凑出和 s；空集凑 0
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        # 倒序更新：每个 x 只用一次（0-1 背包）；正序会把同一 x 重复加
        for s in range(target, x - 1, -1):
            if dp[s - x]:
                dp[s] = True
        if dp[target]:
            print("true")
            return
    print("true" if dp[target] else "false")


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
    cin >> n;  // 读入 n 与数组
    vector<int> nums(n);
    int total = 0;
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
        total += nums[i];
    }
    if (total % 2 != 0) {  // 总和为奇，不可能均分
        cout << "false\n";
        return 0;
    }
    int target = total / 2;
    // 不变量：dp[s] 表示能否凑出和 s；空集凑 0
    vector<char> dp(target + 1, 0);
    dp[0] = 1;
    for (int x : nums) {
        // 倒序更新：每个 x 只用一次（0-1 背包）
        for (int s = target; s >= x; --s) {
            if (dp[s - x]) dp[s] = 1;
        }
        if (dp[target]) {
            cout << "true\n";
            return 0;
        }
    }
    cout << (dp[target] ? "true" : "false") << '\n';
    return 0;
}
```
