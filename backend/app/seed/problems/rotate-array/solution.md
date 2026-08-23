## 思路

- 右旋 k 步等于把后 `k % n` 个元素搬到数组前面。
- 三次翻转实现原地搬移：先整体翻转，再翻转前 k 个，再翻转后 n−k 个。
- 先取 `k %= n`；k 为 0 时数组不变。
- 翻转只交换元素，额外空间 O(1)。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

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
    if n == 0:
        print()
        return
    k %= n
    if k:
        reverse_range(nums, 0, n - 1)
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
    if (n == 0) {
        cout << '\n';
        return 0;
    }
    k %= n;
    if (k) {
        reverse(nums.begin(), nums.end());
        reverse(nums.begin(), nums.begin() + k);
        reverse(nums.begin() + k, nums.end());
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << nums[i];
    }
    cout << '\n';
    return 0;
}
```
