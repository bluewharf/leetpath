## 思路

Kahn：入度为 0 的点入堆，弹出时把它指向的点入度 −1。出队个数小于 n 则有环。

### 解法一（推荐）：最小堆 Kahn

- 边 `a b`：`b → a`，`indeg[a]++`。
- 用堆（而不是普通队列）每次取编号最小的入度 0 节点，保证字典序最小。
- Agent 计划就是 DAG，有环不能执行。

### 解法二：DFS 三色判环 + 逆后序

- 访问中再碰到即环。无环时把结束时间倒过来就是拓扑序。
- 要字典序最小需额外处理，不如堆直接。

## 复杂度

- 解法一：时间 O((n+e) log n)，空间 O(n+e)
- 解法二：时间 O(n+e)，空间 O(n+e)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import heapq
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    idx = 3
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for _ in range(m):
        a, b = data[idx], data[idx + 1]
        graph[b].append(a)
        indeg[a] += 1
        idx += 2
    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    if len(order) < n:
        return
    print(" ".join(map(str, order)))


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
    int n, m, dim;
    cin >> n >> m >> dim;
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        g[b].push_back(a);
        ++indeg[a];
    }
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int i = 0; i < n; ++i)
        if (indeg[i] == 0) heap.push(i);
    vector<int> order;
    while (!heap.empty()) {
        int u = heap.top();
        heap.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (--indeg[v] == 0) heap.push(v);
        }
    }
    if ((int)order.size() < n) return 0;
    for (size_t i = 0; i < order.size(); ++i) {
        if (i) cout << ' ';
        cout << order[i];
    }
    cout << '\n';
    return 0;
}
```
