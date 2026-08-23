## 思路

- 两条链都已有序，用一个指针每次接当前更小的头结点，接到哑节点后面。
- 某条链先走完时，另一条剩余部分本身有序，直接挂上即可。
- 相等时任选一侧（这里取左边），稳定性不影响正确性。
- 空链（长度为 0）读入为 `None`，合并结果自然是另一条链，两条都空则输出 `0`。

## 复杂度

- 时间：O(n1 + n2)
- 空间：O(1)（不计输出链表本身）

## 模板代码

### Python3

```python
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
    print(len(vals))
    if vals:
        print(" ".join(vals))


def merge(l1, l2):
    dummy = ListNode()
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next


def main():
    write_list(merge(read_list(), read_list()))


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
    cout << vals.size() << '\n';
    if (!vals.empty()) {
        for (int i = 0; i < (int)vals.size(); i++) {
            if (i) cout << ' ';
            cout << vals[i];
        }
        cout << '\n';
    }
}

ListNode* merge(ListNode* l1, ListNode* l2) {
    ListNode dummy;
    ListNode* cur = &dummy;
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            cur->next = l1;
            l1 = l1->next;
        } else {
            cur->next = l2;
            l2 = l2->next;
        }
        cur = cur->next;
    }
    cur->next = l1 ? l1 : l2;
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    write_list(merge(read_list(), read_list()));
    return 0;
}
```
