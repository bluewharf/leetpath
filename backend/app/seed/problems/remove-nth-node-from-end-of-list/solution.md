## 思路

- 一次遍历删除倒数第 k 个：快指针先走 k 步，再和慢指针一起走。
- 在头前加 dummy，快慢都从 dummy 出发；快指针走到尾时，慢指针恰好停在待删结点的前驱。
- 删头、删中间、删尾都走同一套 `slow.next = slow.next.next`，不用先数长度。
- 题目保证 k 合法，快指针先走 k 步不会落空。

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


def remove_nth(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    fast = dummy
    for _ in range(k):
        fast = fast.next
    slow = dummy
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next


def main() -> None:
    head, k = read_list()
    write_list(remove_nth(head, k))


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

ListNode* remove_nth(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* fast = &dummy;
    for (int i = 0; i < k; i++) fast = fast->next;
    ListNode* slow = &dummy;
    while (fast->next) {
        slow = slow->next;
        fast = fast->next;
    }
    slow->next = slow->next->next;
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    ListNode* head = read_list(k);
    write_list(remove_nth(head, k));
    return 0;
}
```
