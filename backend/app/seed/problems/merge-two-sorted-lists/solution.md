## 思路

### 解法一：双指针迭代（推荐）

- 两条链都已有序，每次接当前更小的头结点到哑节点后面。
- 某条链先走完时，另一条剩余部分本身有序，直接挂上即可。
- 相等时取左边，稳定性不影响正确性。
- 空链读入为 `None`，合并结果自然是另一条；两条都空则输出 `0`。
- 只改 `next` 指针，额外空间常数，是本题默认写法。

### 解法二：递归

- `merge(l1, l2)`：较小头结点的 `next` 接到「剩下两链的合并结果」上，再返回该头结点。
- 比较规则与迭代相同，代码更短；链很长时递归栈 O(n1+n2)。
- 和迭代差在用调用栈代替哑节点游标。

### 解法三：取值重建

- 把两条链的值拷进数组、排序（或双指针归并到新数组）再重建链表。
- 正确但浪费：输入已经有序，不必再排序，也多一次节点分配。
- 只作对照，提交应原地改指针。

## 复杂度

- 解法一：时间 O(n1+n2)，空间 O(1)（不计输出链表本身）
- 解法二：时间 O(n1+n2)，空间 O(n1+n2)（递归栈）
- 解法三：时间 O(n1+n2)，空间 O(n1+n2)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：双指针接较小头；一侧耗尽则把另一侧剩余直接挂上。
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_list():
    # ACM 读入建链表：先长度后节点值；n=0 为空。与合并算法无关。
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
    # 算法：每次接更小的头；一侧耗尽则把另一侧剩余直接挂上（本身已有序）。
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
// 解法一：双指针接较小头；一侧耗尽则把另一侧剩余直接挂上。
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
    // 双指针接较小头；一侧空则挂上另一侧剩余。
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
