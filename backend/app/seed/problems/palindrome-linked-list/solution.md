## 思路

### 解法一（推荐）：快慢指针 + 反转后半

- 回文意味着前半段与「后半段反转」后逐位相等；用快慢指针一次遍历找中点，不必先拷进数组。
- 快指针每次两步、慢指针一步：偶数长度时慢指针停在前半末尾，奇数长度时停在正中（正中不参与比较）。
- 从慢指针的下一个开始原地反转后半段，再与头指针同步向中间比对，有一处不等即否。
- 空链表和单节点直接是回文。额外只要几个指针。

### 解法二：拷进数组再双指针

- 先遍历链表把值放进数组，然后左右夹逼。
- 实现简单、不会改坏原链表，但额外 O(n) 空间，不是最优。
- 适合先验证题意，再改成解法一。

### 解法三：递归后序对比

- 外层指针从头走，递归走到尾再回溯时与外层比较，相当于用调用栈从后往前扫。
- 空间仍是 O(n)，指针配合容易写错，面试了解即可。
- 和「反转后半」比，它不改链表，但没有把空间降到常数。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)（不计读入建表）
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(n)（递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# —— 建表（I/O）：第一行 n，第二行 n 个值；空表 n=0 ——
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


# —— 算法：快慢指针找中点，原地反转后半，再与前半对撞比对 ——
def is_palindrome(head: ListNode | None) -> bool:
    if head is None or head.next is None:  # 边界：空表/单结点是回文
        return True
    # 偶数时 slow 停在前半末尾，奇数时停在正中（正中不参与比较）
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    pre, cur = None, slow.next
    while cur:  # 反转后半，pre 成为后半新头
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

// —— 建表（I/O）：第一行 n，随后 n 个值；空表 n=0 ——
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

// —— 算法：快慢指针找中点，原地反转后半，再与前半对撞比对 ——
bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;  // 边界：空表/单结点是回文
    // 偶数时 slow 停在前半末尾，奇数时停在正中（正中不参与比较）
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* pre = nullptr;
    ListNode* cur = slow->next;
    while (cur) {  // 反转后半，pre 成为后半新头
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
