## 思路

- 经典哈希表题：边遍历边把"值 → 下标"存进字典。
- 每到一个数 `x`，先查 `target - x` 是否在字典里，在就立即返回答案。
- 这样每个元素只看一次，避免 O(n²) 的双重循环。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1:1 + n]))
    target = int(data[1 + n])
    seen = {}
    for i, x in enumerate(nums):
        j = seen.get(target - x)
        if j is not None:
            print(j, i)
            return
        seen[x] = i

main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    vector<int> nums(n);
    for (auto& x : nums) scanf("%d", &x);
    int target;
    scanf("%d", &target);
    unordered_map<int, int> seen;
    for (int i = 0; i < n; i++) {
        auto it = seen.find(target - nums[i]);
        if (it != seen.end()) {
            printf("%d %d\n", it->second, i);
            return 0;
        }
        seen[nums[i]] = i;
    }
    return 0;
}
```
