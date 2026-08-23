## 思路

- 三路快排 / 荷兰国旗：一次扫描把 `0` 丢到左边、`2` 丢到右边，中间自然是 `1`。
- 三个指针：`lo` 是下一个 `0` 应放的位置，`hi` 是下一个 `2` 应放的位置，`i` 扫描未知区。
- 遇到 `0`：与 `lo` 交换后 `lo++`、`i++`（换过来的只可能是 `0` 或 `1`，已处理过）。
- 遇到 `2`：与 `hi` 交换后只 `hi--`，`i` 不动，因为从右边换来的值还没看过。
- 遇到 `1`：直接 `i++`。循环条件是 `i <= hi`，未知区空了就结束。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    lo, i, hi = 0, 0, n - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1
        else:
            i += 1
    print(*nums)


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
    int lo = 0, i = 0, hi = n - 1;
    while (i <= hi) {
        if (nums[i] == 0) {
            swap(nums[lo], nums[i]);
            lo++;
            i++;
        } else if (nums[i] == 2) {
            swap(nums[i], nums[hi]);
            hi--;
        } else {
            i++;
        }
    }
    for (int j = 0; j < n; j++) {
        if (j) cout << ' ';
        cout << nums[j];
    }
    cout << '\n';
    return 0;
}
```
