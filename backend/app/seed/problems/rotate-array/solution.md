## 思路

### 解法一（推荐）：三次翻转

- 右旋 k 步等于把后 `k % n` 个元素搬到数组前面。
- 三次翻转实现原地搬移：先整体翻转，再翻转前 k 个，再翻转后 n−k 个。
- 先取 `k %= n`；k 为 0 时数组不变。
- 翻转只交换元素，额外空间 O(1)。

### 解法二：额外数组

- 令 `ans[(i + k) % n] = nums[i]`，再拷回原数组。
- 下标映射一眼能看懂，适合先写对再优化空间。
- 和三次翻转比：少了「段反转」的不变量，多 O(n) 空间。

### 解法三：环状替换

- 从下标 `i` 出发，`nums[(j + k) % n]` 被当前值顶替，沿环走一圈；环的个数是 `gcd(k, n)`。
- 同样原地 O(1)，但要数清访问次数，漏环或多走都会写错。
- 面试能讲「置换分解成环」即可，落地仍推三次翻转。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def reverse_range(a: list[int], l: int, r: int) -> None:
    while l < r:
        a[l], a[r] = a[r], a[l]
        l += 1
        r -= 1


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    k = data[n + 1]
    if n == 0:  # 边界：空数组
        print()
        return
    k %= n  # 右旋 k 步 ≡ 后 k%n 个搬到前面
    if k:
        reverse_range(nums, 0, n - 1)  # 整体翻 → 前 k 翻 → 后 n-k 翻
        reverse_range(nums, 0, k - 1)
        reverse_range(nums, k, n - 1)
    print(" ".join(map(str, nums)))


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
    int k;
    cin >> k;
    if (n == 0) {  // 边界：空数组
        cout << '\n';
        return 0;
    }
    k %= n;  // 右旋 k 步 ≡ 后 k%n 个搬到前面
    if (k) {
        reverse(nums.begin(), nums.end());          // 整体翻
        reverse(nums.begin(), nums.begin() + k);    // 前 k 翻
        reverse(nums.begin() + k, nums.end());      // 后 n-k 翻
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << nums[i];
    }
    cout << '\n';
    return 0;
}
```
