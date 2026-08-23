## 思路

- 链表低位在前，正好按竖式从个位加到高位，一边走一边处理进位。
- 循环条件是「任一链表还有节点，或进位还没消化完」，一次覆盖不等长和最高位进位（如 5+5=10）。
- 当前和 `s % 10` 落新节点，`s / 10` 当新进位，和小学加法完全一致。
- 虚头节点省掉「第一个节点要不要特判」；空链表当 0，结果为 0 仍保留单节点。

## 复杂度

- 时间：O(max(n1, n2))
- 空间：O(max(n1, n2))（结果链表；进位只用常数额外变量）

## 模板代码

### Python3

```python
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_list():
    line = sys.stdin.readline()
    if not line:
        return None
    n = int(line.strip())
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
        print(1)
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


def add_two(l1, l2):
    dummy = ListNode()
    cur = dummy
    carry = 0
    while l1 or l2 or carry:
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        carry, digit = divmod(s, 10)
        cur.next = ListNode(digit)
        cur = cur.next
    return dummy.next


def main():
    write_list(add_two(read_list(), read_list()))


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

void write_list(ListNode* head) {
    vector<int> vals;
    for (ListNode* p = head; p; p = p->next) vals.push_back(p->val);
    if (vals.empty()) {
        cout << 1 << '\n' << 0 << '\n';
        return;
    }
    cout << vals.size() << '\n';
    for (size_t i = 0; i < vals.size(); ++i) {
        if (i) cout << ' ';
        cout << vals[i];
    }
    cout << '\n';
}

ListNode* add_two(ListNode* l1, ListNode* l2) {
    ListNode dummy;
    ListNode* cur = &dummy;
    int carry = 0;
    while (l1 || l2 || carry) {
        int s = carry;
        if (l1) {
            s += l1->val;
            l1 = l1->next;
        }
        if (l2) {
            s += l2->val;
            l2 = l2->next;
        }
        carry = s / 10;
        cur->next = new ListNode(s % 10);
        cur = cur->next;
    }
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    write_list(add_two(read_list(), read_list()));
    return 0;
}
```
