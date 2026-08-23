## 思路

- k 路归并：堆里始终放每条链表「当前还未被取走的头结点」，弹出的一定是全局最小。
- 弹出节点后，若该链表还有后继，把后继再丢进堆，这样每条链最多同时占一个堆位。
- 值可能重复，第二关键字用链表下标（同一时刻每条链只有一个节点在堆里，下标唯一），避免节点无法比较。
- 哑节点串起来即可；`k = 0` 或全是空链时堆为空，直接输出空链表。

## 复杂度

- 时间：O(N log k)，N 为节点总数
- 空间：O(k)

## 模板代码

### Python3

```python
import heapq
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_list():
    n = int(sys.stdin.readline())
    if n == 0:
        return None
    vals = list(map(int, sys.stdin.readline().split()))
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def write_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


def merge_k_lists(lists):
    heap = []
    for idx, node in enumerate(lists):
        if node is not None:
            heapq.heappush(heap, (node.val, idx, node))
    dummy = ListNode()
    cur = dummy
    while heap:
        _, idx, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    return dummy.next


def main():
    k = int(sys.stdin.readline())
    lists = [read_list() for _ in range(k)]
    write_list(merge_k_lists(lists))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0) : val(x), next(nullptr) {}
};

ListNode* read_list() {
    int n;
    cin >> n;
    if (n == 0) return nullptr;
    ListNode dummy;
    ListNode* cur = &dummy;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    return dummy.next;
}

void write_list(ListNode* head) {
    vector<int> vals;
    while (head) {
        vals.push_back(head->val);
        head = head->next;
    }
    if (vals.empty()) {
        cout << 0 << '\n';
        return;
    }
    cout << vals.size() << '\n';
    for (int i = 0; i < (int)vals.size(); i++) {
        if (i) cout << ' ';
        cout << vals[i];
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    cin >> k;
    vector<ListNode*> lists(k);
    for (int i = 0; i < k; i++) lists[i] = read_list();
    using T = tuple<int, int, ListNode*>;
    priority_queue<T, vector<T>, greater<T>> heap;
    for (int i = 0; i < k; i++) {
        if (lists[i]) heap.push({lists[i]->val, i, lists[i]});
    }
    ListNode dummy;
    ListNode* cur = &dummy;
    while (!heap.empty()) {
        auto [val, idx, node] = heap.top();
        heap.pop();
        cur->next = node;
        cur = cur->next;
        if (node->next) heap.push({node->next->val, idx, node->next});
    }
    write_list(dummy.next);
    return 0;
}
```
