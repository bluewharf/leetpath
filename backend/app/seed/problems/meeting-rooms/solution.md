## 思路

按开始时间排序，扫一遍看当前开始是否小于上一场结束。

### 解法一（推荐）：排序后线性扫描

- 按 `start` 升序。若 `intervals[i].start < intervals[i-1].end` 则重叠。
- 端点相等不重叠（左闭右开）。
- 空输入为 true。不要做成「选最多场」。

### 解法二：扫事件

- 开始 +1、结束 −1，同一时刻先处理结束。过程中计数超过 1 则有重叠。
- 和「最少会议室」同族，本题只关心峰值是否大于 1。

## 复杂度

- 解法一：时间 O(n log n)，空间 O(1)（不计排序）
- 解法二：时间 O(n log n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        print("true")
        return
    m, n = data[0], data[1]
    iv = []
    idx = 2
    for _ in range(m):
        iv.append((data[idx], data[idx + 1]))
        idx += n
    iv.sort()
    ok = True
    for i in range(1, len(iv)):
        if iv[i][0] < iv[i - 1][1]:
            ok = False
            break
    print("true" if ok else "false")


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
    int m, n;
    if (!(cin >> m >> n)) {
        cout << "true\n";
        return 0;
    }
    vector<pair<int, int>> iv(m);
    for (int i = 0; i < m; ++i) cin >> iv[i].first >> iv[i].second;
    sort(iv.begin(), iv.end());
    bool ok = true;
    for (int i = 1; i < m; ++i) {
        if (iv[i].first < iv[i - 1].second) {
            ok = false;
            break;
        }
    }
    cout << (ok ? "true" : "false") << '\n';
    return 0;
}
```
