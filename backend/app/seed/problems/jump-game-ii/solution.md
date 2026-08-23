## 思路

- 求最少跳数，把数组看成按层扩展的 BFS：当前这一跳能覆盖的区间走完，才必须再跳一次。
- `cur_end` 是「当前跳跃次数」能到达的右边界；扫到边界就 `jumps++`，并把边界更新成这一层探到的最远 `far`。
- 只遍历到 `n - 2`：到达或越过终点时不必再跳，避免在终点处多计一次。
- 题目保证可达，所以不用处理走投无路；`n = 1` 时循环为空，答案 0。
- 贪心正确性：每一跳都把覆盖推到当前能及的最远，少一跳一定覆盖不到这个右端点。

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
    nums = data[1 : n + 1]
    jumps = 0
    cur_end = 0
    far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = far
    print(jumps)


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
    int jumps = 0, cur_end = 0, far = 0;
    for (int i = 0; i < n - 1; i++) {
        far = max(far, i + nums[i]);
        if (i == cur_end) {
            jumps++;
            cur_end = far;
        }
    }
    cout << jumps << "\n";
    return 0;
}
```
