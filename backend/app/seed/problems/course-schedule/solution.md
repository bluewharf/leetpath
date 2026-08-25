## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：Kahn 拓扑排序（推荐）
- 先修关系建成有向图：边 `b → a` 表示修完 `b` 才能修 `a`。
- 能修完全部课 ⟺ 有向图无环 ⟺ 拓扑序长度等于课程数 `n`。
- 入度为 0 的课入队，出队后把后继入度减 1，减到 0 再入队。
- 出队数量小于 `n` 说明有环，输出 `false`；没有先修时队列一开始就装满。
- 模板即此写法，顺带能给出一种上课顺序。

### 解法二：DFS 三色判环
- 每个点三种状态：未访问、正在访问（栈中）、已完成。
- 沿出边 DFS，走到「正在访问」的点就是后向边，图有环。
- 与 Kahn 一样是 O(n+m)；不需要队列和入度数组，但要小心状态恢复。
- 只要判断能否修完、不需要拓扑序列时，DFS 也很常见；本题布尔输出两种都行，落地用解法一更不容易写错。

## 复杂度

- 解法一：时间 O(n + m)，空间 O(n + m)
- 解法二：时间 O(n + m)，空间 O(n + m)（邻接表 + 递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：Kahn 拓扑。能修完全部课 ⟺ 有向图无环 ⟺ 出队数等于 n。
import sys
from collections import deque


def can_finish(n, prerequisites):
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in prerequisites:
        graph[b].append(a)  # 边 b→a：修完 b 才能修 a
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    taken = 0
    while q:
        u = q.popleft()
        taken += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == n  # 出队不足 n 说明有环


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    idx = 3  # 跳过列数 cols（本题固定 2）
    prereq = []
    for _ in range(m):
        prereq.append((data[idx], data[idx + 1]))
        idx += 2
    print("true" if can_finish(n, prereq) else "false")


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：Kahn 拓扑。能修完全部课 ⟺ 有向图无环 ⟺ 出队数等于 n。
#include <bits/stdc++.h>
using namespace std;

bool can_finish(int n, const vector<pair<int, int>>& prerequisites) {
    vector<vector<int>> graph(n);
    vector<int> indeg(n);
    for (auto [a, b] : prerequisites) {
        graph[b].push_back(a);  // 边 b→a：修完 b 才能修 a
        indeg[a]++;
    }
    queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    int taken = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        taken++;
        for (int v : graph[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    return taken == n;  // 出队不足 n 说明有环
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, cols;
    cin >> n >> m >> cols;  // cols 是 ACM 矩阵列数（本题固定 2）
    vector<pair<int, int>> prereq;
    prereq.reserve(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        prereq.push_back({a, b});
    }
    cout << (can_finish(n, prereq) ? "true" : "false") << "\n";
    return 0;
}
```
