## 思路

- 要找的就是升序数组里第一个 `>= target` 的下标，也就是 `lower_bound`。
- 二分维护左闭右开区间 `[lo, hi)`：循环不变量是答案一定落在这个区间内。
- `nums[mid] < target` 时答案在右侧，令 `lo = mid + 1`；否则 `mid` 仍可能是插入点，令 `hi = mid`。
- 结束时 `lo == hi`，这个位置就是插入点；若全部更小则落到 `n`。
- 元素互不相同不影响正确性，相同元素时该写法仍给出最左插入位。

## 复杂度

- 时间：O(log n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    target = data[n + 1]
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    print(lo)


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
    int target;
    cin >> target;
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    cout << lo << '\n';
    return 0;
}
```
