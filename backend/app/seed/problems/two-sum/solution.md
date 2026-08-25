## 思路

### 解法一（推荐）：一遍哈希

- 边扫边把「值 → 下标」放进字典，把两数之和从 O(n²) 变成每次 O(1) 查补数。
- 扫到 `x` 时先问 `target - x` 在不在表里，在就立刻输出；再写入 `x`，避免同一个下标用两次。
- 题目保证恰好一对答案，且补数若存在一定是更早出现的下标，因此自然满足「小下标在前」。
- 相同值也可以（如 `3 3` 配 6）：第一次只入表，第二次才命中，下标不同。

### 解法二：两遍哈希

- 第一遍把所有「值 → 下标」入表（重复值留下较大下标），第二遍对每个 `x` 查 `target - x`。
- 查到的下标必须和当前下标不同，否则 `2x = target` 时会用到自己。
- 与解法一差在：先建完表再查，逻辑分两步更直观，但一定要扫完全部才能开始，无法提前返回。

### 解法三：排序 + 双指针

- 把 `(值, 原下标)` 排序，左右指针按和与 `target` 的大小收缩，命中后按原下标升序输出。
- 正确，但排序破坏了线性扫描，时间 O(n log n)；额外数组存下标。
- 适合「返回值而不是下标」的变体；本题要下标，哈希更直接。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n log n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
