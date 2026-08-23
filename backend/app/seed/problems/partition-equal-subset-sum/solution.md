## 思路

- 能拆成两个等和子集，当且仅当存在一个子集和恰好等于 `total / 2`；总和为奇数时直接不可能。
- 转化成 0-1 背包的可行性问题：`dp[s]` 表示能否凑出和 `s`。
- 每个数 `x` 倒序更新 `dp[s] |= dp[s - x]`，倒序是为了保证每个数只用一次。
- `dp[0] = true` 作起点；一旦 `dp[target]` 变为真就可以提前结束。

## 复杂度

- 时间：O(n · target)，其中 `target = sum(nums) / 2`
- 空间：O(target)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    total = sum(nums)
    if total % 2 != 0:
        print("false")
        return
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
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
    cin >> n;
    vector<int> nums(n);
    int total = 0;
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
        total += nums[i];
    }
    if (total % 2 != 0) {
        cout << "false\n";
        return 0;
    }
    int target = total / 2;
    vector<char> dp(target + 1, 0);
    dp[0] = 1;
    for (int x : nums) {
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
