## 思路

### 解法一：维护 imax / imin（推荐）

- 乘积子数组比求和多一个陷阱：负数会把「当前最大」和「当前最小」对调，所以结尾处两个方向都要记。
- `imax` / `imin` 分别为以当前位置结尾的子数组乘积的最大、最小值；答案是全程 `imax` 的最大值。
- 转移到 `x` 时候选只有三个：单独取 `x`、`imax * x`、`imin * x`（`x < 0` 时后者可能翻成最大）。
- `0` 会把连续乘积清零，等价于从当前元素重新开一段，三个候选已经覆盖。
- 只需扫一遍，不必枚举左右端点；和「只记当前积」的 Kadane 差在必须同时滚最小值。

### 解法二：左右各扫一遍前缀积

- 从左到右累乘，遇 0 把乘数重置为 1；再从右到左一遍。答案取所有前缀/后缀积以及单元素的最大。
- 不含 0 的最优段，一定作为某次从左或从右「未被切断的乘积前缀」出现；含 0 则 0 两侧被重置后分段覆盖。
- 不显式处理负号翻转，靠双向扫描补上「负号在另一侧」的情况。
- 空间同样 O(1)，但要小心重置时机；模板用 imax/imin 一次遍历更直给转移。

### 解法三：枚举右端暴力

- 固定右端，向左累乘并刷新最大，时间 O(n²)。
- 用来对照「为何必须把负号信息压缩进两个状态」；数据稍大即 TLE。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n²)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：同时滚 imax/imin；负数会把最大最小对调，0 等价于另起一段。
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    # imax/imin：以当前位置结尾的子数组乘积的最大/最小值（负数会把二者对调）。
    imax = imin = ans = nums[0]
    for x in nums[1:]:
        cand = (x, imax * x, imin * x)  # 另起一段 / 接最大 / 接最小（x<0 时后者可能翻成最大）
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
// 解法一：同时滚 imax/imin；负数会把最大最小对调，0 等价于另起一段。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    // imax/imin 同时滚：负数翻转最大最小，0 等价于从当前另起一段。
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
