## 思路

- 一遍哈希：边扫边把「值 → 下标」放进字典，把两数之和从 O(n²) 变成每次 O(1) 查补数。
- 扫到 `x` 时先问 `target - x` 在不在表里，在就立刻输出；再写入 `x`，避免同一个下标用两次。
- 题目保证恰好一对答案，且补数若存在一定是更早出现的下标，因此自然满足「小下标在前」。
- 相同值也可以（如 `3 3` 配 6）：第一次只入表，第二次才命中，下标不同。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : n + 1]))
    target = int(data[n + 1])
    seen = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in seen:
            print(seen[y], i)
            return
        seen[x] = i


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
    unordered_map<int, int> seen;
    seen.reserve(n * 2);
    for (int i = 0; i < n; i++) {
        auto it = seen.find(target - nums[i]);
        if (it != seen.end()) {
            cout << it->second << " " << i << "\n";
            return 0;
        }
        seen[nums[i]] = i;
    }
    return 0;
}
```
