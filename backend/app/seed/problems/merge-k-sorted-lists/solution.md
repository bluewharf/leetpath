## 思路

### 解法一：小根堆 k 路归并（推荐）

- 堆里始终放每条链表「当前还未被取走的头结点」，弹出的一定是全局最小。
- 弹出后若该链还有后继，把后继再丢进堆，每条链最多同时占一个堆位。
- 值可能重复，第二关键字用链表下标（同一时刻每条链只有一个节点在堆里，下标唯一），避免节点无法比较。
- 哑节点串起来即可；`k = 0` 或全是空链时堆为空，直接输出空链表。
- 每个节点进出堆一次，对数因子是 k 而不是 N。

### 解法二：分治两两归并

- 把 k 条链对半切，递归合并后再按「合并两个有序列表」接起来。
- 总时间同样 O(N log k)，不依赖堆；递归深度 O(log k)。
- 和堆比：复用 merge-two 代码、常数可能更好，但要写递归分层。

### 解法三：逐条两路合并

- 从空链开始，依次与 `lists[i]` 做两路归并。
- 最坏 O(kN)（链一样长时，后面几次合并都要扫过已经很长的结果），k 大时会 TLE。
- 用来对照「为何要用堆/分治把对数因子留下」。

## 复杂度

- 解法一：时间 O(N log k)，空间 O(k)（N 为节点总数）
- 解法二：时间 O(N log k)，空间 O(log k)（递归栈；不计输出链表）
- 解法三：时间 O(kN)，空间 O(1)（不计输出链表）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：小根堆 k 路归并；每条链同时最多一个节点在堆里，下标当第二关键字。
import heapq
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_list():
    # ACM 读入建链表：先长度后节点值；n=0 为空。与 k 路归并无关。
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
    # 算法：小根堆始终放每条链当前头；弹出全局最小后再把后继塞回去。
    heap = []
    for idx, node in enumerate(lists):
        if node is not None:
            # 值可能重复，用链表下标当第二关键字（同时每条链最多一个节点在堆里）。
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
    lists = [read_list() for _ in range(k)]  # k=0 或全空链时堆为空，输出 0
    write_list(merge_k_lists(lists))


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：小根堆 k 路归并；每条链同时最多一个节点在堆里，下标当第二关键字。
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0) : val(x), next(nullptr) {}
};

ListNode* read_list() {
    // ACM 读入建链表：先长度后节点值；n=0 为空。
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
        if (lists[i]) heap.push({lists[i]->val, i, lists[i]});  // 下标保证值相同时可比较
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
