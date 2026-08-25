## 思路

### 解法一：排序后线性合并（推荐）

- 先按左端点排序，这样可能相交的区间一定相邻（或只与当前「未封闭」的最后一段相交）。
- 当前左端点大于已合并段的右端点：中间有空隙，开一段新的。
- 否则两段有重叠（端点相等也算），把已合并段的右端点改成两者较大者。
- 不变量：`merged` 里的区间始终按左端点有序、两两不交；扫完即是覆盖全集的最简划分。
- 一次排序加线性扫，是合并区间的默认写法。

### 解法二：扫描线

- 把每个左端点记 +1、右端点记 -1，按坐标排序后扫事件；覆盖从 0 变为正是一段开始，变回 0 是一段结束。
- 能顺手求「最多重叠层数」，纯合并区间时比解法一啰嗦。
- 闭区间端点重合要先处理左端再右端，否则会把 `[1,2][2,3]` 拆成两段。

### 解法三：按端点暴力扩展

- 对每个区间向左右看还能不能并进去，用 vis 标记已吸收的区间。
- 时间 O(m²)，用来对照「为何必须先按左端排序」；区间一多就会慢。

## 复杂度

- 解法一：时间 O(m log m)，空间 O(m)
- 解法二：时间 O(m log m)，空间 O(m)
- 解法三：时间 O(m²)，空间 O(m)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：按左端点排序后线性合并；有空隙才新开段，端点相等仍合并。
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    intervals = []
    idx = 2
    for _ in range(m):
        intervals.append((data[idx], data[idx + 1]))
        idx += n
    intervals.sort()  # 按左端点排序后，可能相交的区间一定相邻
    merged = []
    for a, b in intervals:
        if not merged or merged[-1][1] < a:
            merged.append([a, b])  # 与上一段有空隙，开新段（端点相等仍合并）
        elif b > merged[-1][1]:
            merged[-1][1] = b  # 重叠则右端取较大者
    for a, b in merged:
        print(a, b)


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：按左端点排序后线性合并；有空隙才新开段，端点相等仍合并。
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
    sort(intervals.begin(), intervals.end());  // 按左端点；相交段必相邻
    vector<pair<int, int>> merged;
    for (auto [a, b] : intervals) {
        if (merged.empty() || merged.back().second < a) {
            merged.push_back({a, b});  // 有空隙才新开；端点相等仍合并
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
