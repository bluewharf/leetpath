## 思路

- 乘积子数组比求和多一个陷阱：负数会把「当前最大」和「当前最小」对调，所以结尾处两个方向都要记。
- 令 `imax` / `imin` 分别为以当前位置结尾的子数组乘积的最大、最小值；答案是全程 `imax` 的最大值。
- 转移到 `x` 时，候选只有三个：单独取 `x`、`imax * x`、`imin * x`（后者在 `x < 0` 时可能翻成最大）。
- `0` 会把连续乘积清零，等价于从当前元素重新开一段，三个候选已经覆盖这种情况。
- 只需扫一遍，不必真的枚举左右端点。

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
    imax = imin = ans = nums[0]
    for x in nums[1:]:
        cand = (x, imax * x, imin * x)
        imax = max(cand)
        imin = min(cand)
        if imax > ans:
            ans = imax
    print(ans)


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
    long long imax = nums[0], imin = nums[0], ans = nums[0];
    for (int i = 1; i < n; i++) {
        long long x = nums[i];
        long long a = x, b = imax * x, c = imin * x;
        imax = max({a, b, c});
        imin = min({a, b, c});
        ans = max(ans, imax);
    }
    cout << ans << '\n';
    return 0;
}
```
