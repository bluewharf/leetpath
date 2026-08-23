## 思路

- 带 `random` 的链表深拷贝：先把所有新节点造出来，再接线，避免随机指针指向尚未创建的节点。
- 哈希表存「原节点 → 新节点」，`None` 映射到 `None`。
- 第一遍只复制 `val`；第二遍用表把 `next`、`random` 接到对应的新节点上。
- 这样复制链表的指针关系与原链表同构，且不会指回旧节点。
- 输出时再扫一遍新链表，用下标还原 `randomIndex`。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head):
    if head is None:
        return None
    mapping = {None: None}
    cur = head
    while cur:
        mapping[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        mapping[cur].next = mapping[cur.next]
        mapping[cur].random = mapping[cur.random]
        cur = cur.next
    return mapping[head]


def main():
    n = int(sys.stdin.readline())
    if n == 0:
        print(0)
        return
    vals = []
    rands = []
    for _ in range(n):
        parts = sys.stdin.readline().split()
        vals.append(int(parts[0]))
        rands.append(int(parts[1]))
    nodes = [Node(v) for v in vals]
    for i in range(n):
        if i + 1 < n:
            nodes[i].next = nodes[i + 1]
        if rands[i] != -1:
            nodes[i].random = nodes[rands[i]]
    copied = copy_random_list(nodes[0])
    arr = []
    cur = copied
    while cur:
        arr.append(cur)
        cur = cur.next
    idx = {node: i for i, node in enumerate(arr)}
    print(len(arr))
    for node in arr:
        ri = idx[node.random] if node.random is not None else -1
        print(node.val, ri)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int val;
    Node *next, *random;
    Node(int x) : val(x), next(nullptr), random(nullptr) {}
};

Node* copy_random_list(Node* head) {
    if (!head) return nullptr;
    unordered_map<Node*, Node*> mapping;
    mapping[nullptr] = nullptr;
    Node* cur = head;
    while (cur) {
        mapping[cur] = new Node(cur->val);
        cur = cur->next;
    }
    cur = head;
    while (cur) {
        mapping[cur]->next = mapping[cur->next];
        mapping[cur]->random = mapping[cur->random];
        cur = cur->next;
    }
    return mapping[head];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n == 0) {
        cout << 0 << "\n";
        return 0;
    }
    vector<int> vals(n), rands(n);
    for (int i = 0; i < n; i++) cin >> vals[i] >> rands[i];
    vector<Node*> nodes(n);
    for (int i = 0; i < n; i++) nodes[i] = new Node(vals[i]);
    for (int i = 0; i < n; i++) {
        if (i + 1 < n) nodes[i]->next = nodes[i + 1];
        if (rands[i] != -1) nodes[i]->random = nodes[rands[i]];
    }
    Node* copied = copy_random_list(nodes[0]);
    vector<Node*> arr;
    for (Node* cur = copied; cur; cur = cur->next) arr.push_back(cur);
    unordered_map<Node*, int> idx;
    for (int i = 0; i < (int)arr.size(); i++) idx[arr[i]] = i;
    cout << arr.size() << "\n";
    for (Node* node : arr) {
        int ri = node->random ? idx[node->random] : -1;
        cout << node->val << " " << ri << "\n";
    }
    return 0;
}
```
