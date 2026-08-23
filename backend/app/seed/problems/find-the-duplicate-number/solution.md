## 思路

- 值域 `[1, n]`、长度 `n+1`，把下标 i 看成指向 `nums[i]` 的指针，数组就是一张有环的函数图。
- 重复值意味着有两个入口指向同一个节点，环的入口就是那个重复数。
- Floyd：快慢指针先相遇证明有环，再把慢指针拉回起点同步走，第二次相遇必在环入口。
- 值从 1 开始，0 不会被任何节点指向，从 `nums[0]` 出发一定能进环。
- 全程只读两个指针，满足「不改数组 + O(1) 额外空间」。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    print(slow)


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
    int slow = nums[0], fast = nums[0];
    while (true) {
        slow = nums[slow];
        fast = nums[nums[fast]];
        if (slow == fast) break;
    }
    slow = nums[0];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    cout << slow << "\n";
    return 0;
}
```
