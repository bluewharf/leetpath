## 思路

- 先按左端点排序，这样可能相交的区间一定相邻（或只与当前「未封闭」的最后一段相交）。
- 从左到右扫：若当前左端点大于已合并段的右端点，说明中间有空隙，开一段新的。
- 否则两段有重叠（端点相等也算），把已合并段的右端点改成两者较大者。
- 不变量：`merged` 里的区间始终按左端点有序、两两不交；扫完即是覆盖全集的最简划分。

## 复杂度

- 时间：O(m log m)
- 空间：O(m)

## 模板代码

### Python3

```python
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    intervals = []
    idx = 2
    for _ in range(m):
        intervals.append((data[idx], data[idx + 1]))
        idx += n
    intervals.sort()
    merged = []
    for a, b in intervals:
        if not merged or merged[-1][1] < a:
            merged.append([a, b])
        elif b > merged[-1][1]:
            merged[-1][1] = b
    for a, b in merged:
        print(a, b)


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
    cin >> m >> n;
    vector<pair<int, int>> intervals(m);
    for (int i = 0; i < m; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }
    sort(intervals.begin(), intervals.end());
    vector<pair<int, int>> merged;
    for (auto [a, b] : intervals) {
        if (merged.empty() || merged.back().second < a) {
            merged.push_back({a, b});
        } else if (b > merged.back().second) {
            merged.back().second = b;
        }
    }
    for (auto [a, b] : merged) {
        cout << a << ' ' << b << '\n';
    }
    return 0;
}
```
