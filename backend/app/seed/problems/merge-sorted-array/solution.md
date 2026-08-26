## 思路

双指针从左往右比，小的写入结果，谁先走完就把另一边拷过去。

### 解法一（推荐）：新数组双指针

- `i`、`j` 指向两个数组头部，比较后写入。
- 时间 O(n+m)，空间 O(n+m)。稳定。
- 空数组和全小全大先写。

### 解法二：原地（力扣 88 形态）

- 若题面保证 `nums1` 尾部有空位，从右往左填，避免覆盖。本题按两个独立数组输出，不必原地。

## 复杂度

- 解法一：时间 O(n+m)，空间 O(n+m)
- 解法二：时间 O(n+m)，空间 O(1)（在 nums1 上）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    idx = 0
    n = data[idx]
    idx += 1
    a = data[idx : idx + n]
    idx += n
    m = data[idx]
    idx += 1
    b = data[idx : idx + m]
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    print(" ".join(map(str, out)))


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
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    int m;
    cin >> m;
    vector<int> b(m);
    for (int i = 0; i < m; ++i) cin >> b[i];
    vector<int> out;
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] <= b[j]) out.push_back(a[i++]);
        else out.push_back(b[j++]);
    }
    while (i < n) out.push_back(a[i++]);
    while (j < m) out.push_back(b[j++]);
    for (size_t k = 0; k < out.size(); ++k) {
        if (k) cout << ' ';
        cout << out[k];
    }
    cout << '\n';
    return 0;
}
```
