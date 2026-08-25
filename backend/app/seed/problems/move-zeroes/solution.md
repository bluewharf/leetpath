## 思路

### 解法一：快慢指针覆盖再填零（推荐）

- 要保持非零元素相对顺序，本质是把非零稳定地「压到前面」，零填到剩下的尾部。
- 慢指针 `write` 指向下一个该放非零的位置；快指针扫全数组，遇到非零就写到 `write` 并右移。
- 扫完后 `[write, n)` 全部置 0，相对顺序自然保留，且只额外用常数空间。
- `n = 0` 时按约定打一个空行。
- 每个非零最多写一次，零在第二趟统一填，读写次数少。

### 解法二：快慢指针交换

- `write` 仍指向下一个非零坑，遇到非零就与 `nums[write]` 交换再 `write++`。
- 一次遍历完成：`write` 左侧已是非零原顺序，右侧是被换过来的零和尚未处理的元素。
- 和覆盖法比：少一次填零循环，但交换可能把零提前写到中间，赋值次数略多。

### 解法三：额外数组

- 先把非零按顺序拷到新数组再补零，最后写回。
- 稳定且好写，空间 O(n)；本题要求原地时应解法一。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
