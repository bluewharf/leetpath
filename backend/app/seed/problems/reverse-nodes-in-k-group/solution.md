## 思路

### 解法一（推荐）：迭代按组反转

- 按组处理：先从当前组前驱出发数出第 k 个结点；不够 k 个就整段保持原序并结束。
- 有完整的 k 个时，把这一段当成普通链表反转（迭代拧指针），接到下一段的开头。
- dummy 记住整条链的入口；反转后原组头变成组尾，作为下一组的前驱。
- 必须改指针，不能只交换结点值。

### 解法二：递归

- 先从头数 k 个，不够则原样返回；够则反转这 k 个，尾接到 `reverseKGroup(rest, k)`。
- 代码更短，把「后面的组」交给递归，和「反转链表」的递归版同一思路。
- 递归栈 O(n/k)，空间不如迭代常数。

### 解法三：栈

- 每积累 k 个就弹出接上；不足 k 个按原序接到答案后面。
- 额外 O(k) 空间，relink 时要同时维护新链尾和未处理前缀，容易写乱。
- 适合先用栈想清楚组内顺序，再改回解法一的原地拧指针。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n/k)
- 解法三：时间 O(n)，空间 O(k)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# —— 建表（I/O）：n 与结点值后跟 k ——
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


# —— 算法：按组数满 k 才反转；不足 k 的尾段保持原序 ——
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:  # 本段不够 k 个，整段不动并结束
                return dummy.next
        group_next = kth.next
        # prev 初值接到下一组头，反转后原组头自然链向下一段
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        tail = group_prev.next  # 原组头变成组尾，作为下一组前驱
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

// —— 建表（I/O）：n 与结点值后跟 k ——
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

// —— 算法：按组数满 k 才反转；不足 k 的尾段保持原序 ——
ListNode* reverse_k_group(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    while (true) {
        ListNode* kth = groupPrev;
        for (int i = 0; i < k; i++) {
            kth = kth->next;
            if (!kth) return dummy.next;  // 本段不够 k 个，整段不动并结束
        }
        ListNode* groupNext = kth->next;
        ListNode* prev = groupNext;  // 初值接到下一组头，反转后原组头自然链向下一段
        ListNode* cur = groupPrev->next;
        while (cur != groupNext) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        ListNode* tail = groupPrev->next;  // 原组头变成组尾，作为下一组前驱
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
