## 思路

### 解法一：双指针归并（推荐）

- 两数组都已有序，用双指针归并得到总长 `tot = n + m` 的有序序列。
- 中位数只看正中间：奇数取 `merged[tot//2]`；偶数取中间两个的平均值。
- 某一侧为空时对应指针一开始就越界，归并自然退化成拷贝另一侧。
- 本题 `n + m ≤ 2000`，线性合并足够；输出按约定保留 1 位小数。
- 和二分划分比：先得到整体有序再取中位，实现短、边界少，不压对数时间。

### 解法二：二分划分点

- 在较短数组上二分切分，使左半总个数 = `(n+m+1)//2`，且 `max(左半) ≤ min(右半)`。
- 用 `a[i-1] ≤ b[j]` 与 `b[j-1] ≤ a[i]` 判断切分是否合法，过大过小则收缩边界；空侧用 ±∞ 哨兵。
- 中位数由左半最大值、右半最小值拼出。
- 时间 `O(log(min(n,m)))`，面试常追问的最优解，切分边界比归并多，容易写歪。

### 解法三：第 k 小

- 偶数中位数是第 `tot/2` 与第 `tot/2+1` 小的平均，奇数是第 `(tot+1)/2` 小。
- 每次比较两数组各自的第 `k/2` 个，丢弃较小的那一段，递归找第 `k - k/2` 小。
- 与划分点本质同类，写成「删掉不可能的前缀」更好背；实现仍是对数，模板用归并即可过。

## 复杂度

- 解法一：时间 O(n+m)，空间 O(n+m)
- 解法二：时间 O(log(min(n,m)))，空间 O(1)
- 解法三：时间 O(log(n+m))，空间 O(log(n+m))（递归；可改迭代为 O(1)）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

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
