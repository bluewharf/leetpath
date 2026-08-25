## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：Floyd 再找入口（推荐）

- 先用 Floyd 找到相遇点，证明有环；找不到则无环，输出 `-1`。
- 设环外长 a、环长 c、相遇时慢针在环内走了 b，则 `2(a+b) = a+b+kc` ⇒ `a = kc-b`，即「从头再走 a」等于「从相遇点再走完剩下的环」。
- 因此一个指针从头出发，一个从相遇点出发，同步各走一步，相遇处就是入环节点。
- 环入口在头节点时同样成立：第二次遍历会在头上碰上。
- 本题输出入环节点的值，不是下标；无环（含空链表）输出 `-1`。

### 解法二：哈希表记首次位置

- 沿 next 走，第一个重复出现的节点就是入口；走到空则无环，输出 -1。
- 时间线性、空间线性，能找到入口但不满足 O(1) 空间。
- 面试要能把 Floyd 的第二阶段（入口等式）讲圆，不能只停在「相遇即有环」。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    if n == 0:
        print(-1)
        return
    vals = list(map(int, data[1 : 1 + n]))
    pos = int(data[1 + n])
    # 建链：pos>=0 时尾接到 nodes[pos] 成环；无环（含空）输出 -1
    nodes = [ListNode(v) for v in vals]
    for i in range(n - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < n:
        nodes[-1].next = nodes[pos]
    slow = fast = nodes[0]
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # 相遇后再让一个从头同步走，碰上即入口；输出节点值不是下标
            p = nodes[0]
            while p is not slow:
                p = p.next
                slow = slow.next
            print(p.val)
            return
    print(-1)


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
    ListNode(int x) : val(x), next(nullptr) {}
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n == 0) {
        cout << -1 << "\n";
        return 0;
    }
    vector<ListNode*> nodes(n);
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        nodes[i] = new ListNode(v);
    }
    for (int i = 0; i < n - 1; i++) nodes[i]->next = nodes[i + 1];
    int pos;
    cin >> pos;
    // 建链：pos>=0 时尾接到 nodes[pos] 成环；无环（含空）输出 -1
    if (pos >= 0 && pos < n) nodes[n - 1]->next = nodes[pos];
    ListNode* slow = nodes[0];
    ListNode* fast = nodes[0];
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            // 相遇后再让一个从头同步走，碰上即入口；输出节点值不是下标
            ListNode* p = nodes[0];
            while (p != slow) {
                p = p->next;
                slow = slow->next;
            }
            cout << p->val << "\n";
            return 0;
        }
    }
    cout << -1 << "\n";
    return 0;
}
```
