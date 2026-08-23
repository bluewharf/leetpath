## 思路

- 两数组都已有序，用双指针归并即可得到总长 `tot = n + m` 的有序序列。
- 中位数只看正中间：奇数取 `merged[tot//2]`；偶数取中间两个的平均值。
- 某一侧为空时，对应指针一开始就越界，归并自然退化成拷贝另一侧。
- 本题 `n + m ≤ 2000`，线性合并足够；面试若卡 `O(log(min(n, m)))`，再改成在较短数组上二分划分点。
- 输出按约定保留 1 位小数。

## 复杂度

- 时间：O(n + m)
- 空间：O(n + m)

## 模板代码

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1 : 1 + n]
    m = data[1 + n]
    b = data[2 + n : 2 + n + m]
    i = j = 0
    merged = []
    while i < n and j < m:
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    tot = n + m
    mid = tot // 2
    if tot % 2:
        med = float(merged[mid])
    else:
        med = (merged[mid - 1] + merged[mid]) / 2.0
    print(f"{med:.1f}")


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
    for (int i = 0; i < n; i++) cin >> a[i];
    int m;
    cin >> m;
    vector<int> b(m);
    for (int i = 0; i < m; i++) cin >> b[i];
    vector<int> merged;
    merged.reserve(n + m);
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] <= b[j]) merged.push_back(a[i++]);
        else merged.push_back(b[j++]);
    }
    while (i < n) merged.push_back(a[i++]);
    while (j < m) merged.push_back(b[j++]);
    int tot = n + m;
    int mid = tot / 2;
    double med;
    if (tot % 2) med = merged[mid];
    else med = (merged[mid - 1] + merged[mid]) / 2.0;
    cout << fixed << setprecision(1) << med << '\n';
    return 0;
}
```
