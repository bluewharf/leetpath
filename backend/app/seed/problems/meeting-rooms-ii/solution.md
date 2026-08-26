## 思路

同时进行的最大场数就是最少房间数。把开始、结束当事件扫描。

### 解法一（推荐）：差分数 / 扫描线

- 开始时刻 +1，结束时刻 −1。同一时刻先处理结束再处理开始，这样相接不占两间。
- 扫的过程取峰值。
- 空输入答案 0。

### 解法二：双指针

- 开始数组、结束数组分别排序。用指针走开始：若当前开始 < 当前结束则需要新房间，否则释放一间。
- 和扫描线等价。

## 复杂度

- 解法一：时间 O(n log n)，空间 O(n)
- 解法二：时间 O(n log n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        print(0)
        return
    m, n = data[0], data[1]
    events = []
    idx = 2
    for _ in range(m):
        s, e = data[idx], data[idx + 1]
        events.append((s, 1))
        events.append((e, -1))
        idx += n
    events.sort(key=lambda x: (x[0], x[1]))  # 同一时刻先结束
    cur = ans = 0
    for _, d in events:
        cur += d
        if cur > ans:
            ans = cur
    print(ans)


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
        cout << 0 << '\n';
        return 0;
    }
    vector<pair<int, int>> events;
    for (int i = 0; i < m; ++i) {
        int s, e;
        cin >> s >> e;
        events.push_back({s, 1});
        events.push_back({e, -1});
    }
    sort(events.begin(), events.end(), [](auto& a, auto& b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second < b.second;  // 同一时刻先结束
    });
    int cur = 0, ans = 0;
    for (auto [t, d] : events) {
        cur += d;
        ans = max(ans, cur);
    }
    cout << ans << '\n';
    return 0;
}
```
