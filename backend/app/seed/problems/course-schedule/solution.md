## 思路

- 先修关系建成有向图：边 `b → a` 表示修完 `b` 才能修 `a`。
- 能修完全部课 ⟺ 有向图无环 ⟺ 拓扑序长度等于课程数 `n`。
- Kahn：入度为 0 的课入队，出队后把后继入度减 1，减到 0 再入队。
- 出队数量小于 `n` 说明有环，输出 `false`。
- 没有先修时所有点入度为 0，队列一开始就装满，答案为 `true`。

## 复杂度

- 时间：O(n + m)
- 空间：O(n + m)

## 模板代码

### Python3

```python
import sys
from collections import deque


def can_finish(n, prerequisites):
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in prerequisites:
        graph[b].append(a)
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
    return taken == n


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    idx = 3
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
#include <bits/stdc++.h>
using namespace std;

bool can_finish(int n, const vector<pair<int, int>>& prerequisites) {
    vector<vector<int>> graph(n);
    vector<int> indeg(n);
    for (auto [a, b] : prerequisites) {
        graph[b].push_back(a);
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
    return taken == n;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, cols;
    cin >> n >> m >> cols;
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
