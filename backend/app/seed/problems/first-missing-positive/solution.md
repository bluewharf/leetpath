## 思路

- 缺失的最小正整数只可能是 `1..n+1`：出现过的正数最多把 `1..n` 全部填满。
- 把数组本身当哈希表：值为 x∈[1,n] 的数应放到下标 x-1。
- 用交换把每个合法 x 归位；若目标槽已经是 x，立刻停，避免重复值死循环。
- 负数、0、大于 n 的数都是垃圾，占着槽位也没关系，它们不会被当成「已归位」。
- 再扫一遍，第一个 `nums[i] != i+1` 的位置就是答案；若全对，缺的是 n+1。

## 复杂度

- 时间：O(n)
- 空间：O(1) 额外空间（就地交换）

## 模板代码

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0]) if data else 0
    nums = list(map(int, data[1 : 1 + n]))
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            print(i + 1)
            return
    print(n + 1)


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
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int j = nums[i] - 1;
            swap(nums[i], nums[j]);
        }
    }
    for (int i = 0; i < n; i++) {
        if (nums[i] != i + 1) {
            cout << i + 1 << "\n";
            return 0;
        }
    }
    cout << n + 1 << "\n";
    return 0;
}
```
