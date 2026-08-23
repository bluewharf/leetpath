## 思路

- Kadane：只关心「以 i 结尾」的最大子数组和，答案是这些值里的全局最大。
- 转移很短：`cur = max(nums[i], cur + nums[i])`——前面那段和若已经变负，再往后加只会拖后腿，直接从当前元素另起一段。
- 不变量：扫完 i 时，`cur` 一定是所有以 i 结尾的连续段里和最大的那个。
- 全是负数时，算法会不断「另起一段」，最终落到最大的那个单元素，不会误返回 0。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur + x < x else cur + x
        if cur > best:
            best = cur
    print(best)


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
    vector<long long> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    long long best = nums[0], cur = nums[0];
    for (int i = 1; i < n; i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    cout << best << '\n';
    return 0;
}
```
