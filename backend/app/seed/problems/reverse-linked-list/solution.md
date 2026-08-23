## 思路

- 迭代三指针反转：`prev` / `cur` / `nxt`，把每条边的方向拧过来。
- 保存 `cur.next` 后，把 `cur.next` 改指 `prev`，再整体前移一格。
- 循环结束时 `prev` 就是新头；空链表、单结点自然正确。
- 不需要递归：迭代已经是 O(1) 额外空间的标准写法。

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


def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def main() -> None:
    write_list(reverse_list(read_list()))


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
    for (size_t i = 0; i < vals.size(); i++) {
        if (i) cout << ' ';
        cout << vals[i];
    }
    cout << '\n';
}

ListNode* reverse_list(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    write_list(reverse_list(read_list()));
    return 0;
}
```
