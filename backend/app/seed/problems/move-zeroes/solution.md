## 思路

- 要保持非零元素相对顺序，本质是把非零稳定地「压到前面」，零填到剩下的尾部。
- 慢指针 `write` 指向下一个该放非零的位置；快指针扫全数组，遇到非零就写到 `write` 并右移。
- 扫完后 `[write, n)` 全部置 0，相对顺序自然保留，且只额外用常数空间。
- `n = 0` 时按约定打一个空行。

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
    write = 0
    for x in nums:
        if x != 0:
            nums[write] = x
            write += 1
    for i in range(write, n):
        nums[i] = 0
    if n:
        print(" ".join(map(str, nums)))
    else:
        print()


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
    int write = 0;
    for (int x : nums) {
        if (x != 0) nums[write++] = x;
    }
    for (int i = write; i < n; i++) nums[i] = 0;
    if (n == 0) {
        cout << '\n';
    } else {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << nums[i];
        }
        cout << '\n';
    }
    return 0;
}
```
