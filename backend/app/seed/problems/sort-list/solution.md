## 思路

- 链表不能下标随机访问，适合归并排序：每次对半切开、递归排序、再合并两条有序链。
- 用快慢指针找中点：`fast` 走两步、`slow` 走一步，断开 `slow` 与后半的连接，保证两段长度相差不超过 1。
- 合并与「合并两个有序链表」相同，哑结点接较小头，剩余整段挂上。
- 递归出口是空链或单结点；自底向上长度倍增，整体 O(n log n)。
- 递归深度是 O(log n)，满足链表排序的空间约束。

## 复杂度

- 时间：O(n log n)
- 空间：O(log n)（递归栈）

## 模板代码

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def read_list() -> ListNode | None:
    data = sys.stdin.read().split()
    n = int(data[0])
    if n == 0:
        return None
    dummy = ListNode()
    cur = dummy
    for v in data[1 : 1 + n]:
        cur.next = ListNode(int(v))
        cur = cur.next
    return dummy.next


def write_list(head: ListNode | None) -> None:
    vals: list[str] = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


def split(head: ListNode) -> ListNode:
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    return mid


def merge(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 if l1 else l2
    return dummy.next


def sort_list(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    mid = split(head)
    return merge(sort_list(head), sort_list(mid))


def main() -> None:
    write_list(sort_list(read_list()))


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
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* split(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* mid = slow->next;
    slow->next = nullptr;
    return mid;
}

ListNode* mergeList(ListNode* l1, ListNode* l2) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}

ListNode* sortList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* mid = split(head);
    return mergeList(sortList(head), sortList(mid));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n) || n == 0) {
        cout << 0 << '\n';
        return 0;
    }
    ListNode dummy;
    ListNode* cur = &dummy;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    ListNode* head = sortList(dummy.next);
    vector<int> vals;
    for (ListNode* p = head; p; p = p->next) vals.push_back(p->val);
    if (vals.empty()) {
        cout << 0 << '\n';
        return 0;
    }
    cout << vals.size() << '\n';
    for (size_t i = 0; i < vals.size(); i++) {
        if (i) cout << ' ';
        cout << vals[i];
    }
    cout << '\n';
    return 0;
}
```
