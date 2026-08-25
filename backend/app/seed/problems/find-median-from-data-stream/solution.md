## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：对顶堆（推荐）

- 动态中位数用两个堆对半分：大顶堆 `lo` 存较小一半，小顶堆 `hi` 存较大一半。
- 不变量：`lo` 比 `hi` 多 0 或 1 个元素，因此 `lo` 堆顶永远是「下中位数」。
- 新数先推进 `lo`，立刻把 `lo` 的最大值挪到 `hi`；若 `hi` 更长再挪回来，保证对半分且有序。
- 奇数个元素时中位数就是 `lo` 顶；偶数个取两堆顶的平均值。
- 每次插入 O(log n)、查询 O(1)，不必每次全排序。

### 解法二：有序容器插入

- 用有序数组或平衡树（`multiset`）保持全部数字有序，中位数就是中间一或两个位置。
- 数组每次插入要挪元素，单次 O(n)；平衡树插入 O(log n)，但要额外维护中位迭代器。
- 查询仍可做到 O(1) 或 O(log n)，空间同样线性，只是「多存了用不上的顺序」。
- 数据流只关心分界处，对顶堆更贴考点，有序容器当作对照即可。

## 复杂度

- 解法一：时间 O(q log q)（每次 addNum 堆操作 O(log k)），空间 O(q)
- 解法二：时间数组插入合计 O(q²) / 平衡树 O(q log q)，空间 O(q)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import heapq
import sys


class MedianFinder:
    def __init__(self):
        # 对顶堆：lo 较小半（大顶，存相反数），hi 较大半（小顶）
        self.lo = []
        self.hi = []

    def addNum(self, num):
        # 先入 lo 再把最大值挪到 hi；hi 更长则挪回，保证 lo 比 hi 多 0 或 1
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        # 奇数个取 lo 顶；偶数个取两堆顶平均
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


def main():
    q = int(sys.stdin.readline())
    mf = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "MedianFinder":
            mf = MedianFinder()
            print("null")
        elif op == "addNum":
            mf.addNum(int(parts[1]))
            print("null")
        elif op == "findMedian":
            print(f"{mf.findMedian():.1f}")


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class MedianFinder {
    // 对顶堆：lo 较小半（大顶），hi 较大半（小顶）；lo 比 hi 多 0 或 1
    priority_queue<int> lo;
    priority_queue<int, vector<int>, greater<int>> hi;

public:
    void addNum(int num) {
        // 先入 lo 再把最大值挪到 hi；hi 更长则挪回，维持对半分
        lo.push(num);
        hi.push(lo.top());
        lo.pop();
        if ((int)hi.size() > (int)lo.size()) {
            lo.push(hi.top());
            hi.pop();
        }
    }

    double findMedian() {
        // 奇数个取 lo 顶；偶数个取两堆顶平均
        if (lo.size() > hi.size()) return (double)lo.top();
        return (lo.top() + hi.top()) / 2.0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    MedianFinder mf;
    cout << fixed << setprecision(1);
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "MedianFinder") {
            cout << "null\n";
        } else if (op == "addNum") {
            int x;
            cin >> x;
            mf.addNum(x);
            cout << "null\n";
        } else if (op == "findMedian") {
            cout << mf.findMedian() << "\n";
        }
    }
    return 0;
}
```
