## 思路

- 贪心维护「从起点出发目前能摸到的最远下标 `far`」，不必搜索所有跳法。
- 扫描到 i 时若 `i > far`，说明前面所有可达位置都跳不过来，后面更到不了，直接判失败。
- 否则用 `i + nums[i]` 刷新 `far`：当前位置能跳到的更远处，成为新的可达上界。
- 不变量：循环进行到 i 时，`[0, far]` 都可达；能扫完全程则终点必在这个区间里。
- `n = 1` 已经站在终点，无论 `nums[0]` 是不是 0 都成功。

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
    far = 0
    for i in range(n):
        if i > far:
            print("false")
            return
        far = max(far, i + nums[i])
    print("true")


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
    int far = 0;
    for (int i = 0; i < n; i++) {
        if (i > far) {
            cout << "false\n";
            return 0;
        }
        far = max(far, i + nums[i]);
    }
    cout << "true\n";
    return 0;
}
```
