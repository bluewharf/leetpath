## 思路

- 回文意味着前半段与「后半段反转」后逐位相等；用快慢指针一次遍历找到中点，不必先拷进数组。
- 快指针每次两步、慢指针一步：偶数长度时慢指针停在前半末尾，奇数长度时停在正中（正中节点不参与比较）。
- 从慢指针的下一个开始原地反转后半段，再与头指针同步向中间比对，有一处不等即否。
- 空链表和单节点直接是回文。额外只要几个指针，空间 O(1)。

## 复杂度

- 时间：O(n)
- 空间：O(1)（不计读入建表）

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


def is_palindrome(head: ListNode | None) -> bool:
    if head is None or head.next is None:
        return True
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    pre, cur = None, slow.next
    while cur:
        nxt = cur.next
        cur.next = pre
        pre, cur = cur, nxt
    while pre:
        if pre.val != head.val:
            return False
        pre = pre.next
        head = head.next
    return True


def main() -> None:
    print("true" if is_palindrome(read_list()) else "false")


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
    ListNode(int v = 0) : val(v), next(nullptr) {}
};

ListNode* readList() {
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    ListNode dummy;
    ListNode* cur = &dummy;
    for (int i = 0; i < n; ++i) {
        int v;
        cin >> v;
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    return dummy.next;
}

bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* pre = nullptr;
    ListNode* cur = slow->next;
    while (cur) {
        ListNode* nxt = cur->next;
        cur->next = pre;
        pre = cur;
        cur = nxt;
    }
    while (pre) {
        if (pre->val != head->val) return false;
        pre = pre->next;
        head = head->next;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << (isPalindrome(readList()) ? "true" : "false") << '\n';
    return 0;
}
```
