## 思路

- 按组处理：先从当前组前驱出发数出第 k 个结点；不够 k 个就整段保持原序并结束。
- 有完整的 k 个时，把这一段当成普通链表反转（迭代拧指针），接到下一段的开头。
- dummy 记住整条链的入口；反转后原组头变成组尾，作为下一组的前驱。
- 必须改指针，不能只交换结点值。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def read_list() -> tuple[ListNode | None, int]:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    if n == 0:
        return None, data[1]
    dummy = ListNode()
    cur = dummy
    for v in data[1 : 1 + n]:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next, data[1 + n]


def write_list(head: ListNode | None) -> None:
    vals: list[str] = []
    while head:
        vals.append(str(head.val))
        head = head.next
    print(len(vals))
    if vals:
        print(" ".join(vals))


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        tail = group_prev.next
        group_prev.next = kth
        group_prev = tail


def main() -> None:
    head, k = read_list()
    write_list(reverse_k_group(head, k))


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

ListNode* read_list(int& k) {
    int n;
    cin >> n;
    if (n == 0) {
        cin >> k;
        return nullptr;
    }
    ListNode dummy;
    ListNode* cur = &dummy;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    cin >> k;
    return dummy.next;
}

void write_list(ListNode* head) {
    vector<int> vals;
    while (head) {
        vals.push_back(head->val);
        head = head->next;
    }
    cout << vals.size() << '\n';
    if (!vals.empty()) {
        for (size_t i = 0; i < vals.size(); i++) {
            if (i) cout << ' ';
            cout << vals[i];
        }
        cout << '\n';
    }
}

ListNode* reverse_k_group(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    while (true) {
        ListNode* kth = groupPrev;
        for (int i = 0; i < k; i++) {
            kth = kth->next;
            if (!kth) return dummy.next;
        }
        ListNode* groupNext = kth->next;
        ListNode* prev = groupNext;
        ListNode* cur = groupPrev->next;
        while (cur != groupNext) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        ListNode* tail = groupPrev->next;
        groupPrev->next = kth;
        groupPrev = tail;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    ListNode* head = read_list(k);
    write_list(reverse_k_group(head, k));
    return 0;
}
```
