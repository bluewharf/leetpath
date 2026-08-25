## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：模拟竖式 + 虚头节点（推荐）
- 链表低位在前，正好按竖式从个位加到高位，一边走一边处理进位。
- 循环条件是「任一链表还有节点，或进位还没消化完」，一次覆盖不等长和最高位进位（如 `5+5=10`）。
- 当前和 `s % 10` 落新节点，`s / 10` 当新进位，和小学加法完全一致。
- 虚头省掉「第一个节点要不要特判」；空链表当 0，结果为 0 仍保留单节点。
- 模板就是一遍迭代，额外只用常数个指针和进位变量。

### 解法二：递归相加
- `add(l1, l2, carry)`：当前位是两节点值（缺席当 0）加进位，余数做新节点，商传给下一层。
- 递归出口：两指针都空且进位为 0。
- 与解法一不变量相同，只是把循环展开成调用栈；长短不一、最高位进位都自然落在递归参数里。
- 时间同为 O(max(n1, n2))，但递归深度最坏等于结果长度，链很长时有爆栈风险。
- 白板若迭代指针容易乱，可用递归把「当前位 / 进位 / 后继」说清楚，落地仍推荐解法一。

## 复杂度

- 解法一：时间 O(max(n1, n2))，空间 O(1)（不计结果链表）
- 解法二：时间 O(max(n1, n2))，空间 O(max(n1, n2))（递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：按竖式从低位加到高位，虚头省掉首节点特判。
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_list():
    # ACM 读入建链表：先长度后节点值；空链当 0。
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
    while l1 or l2 or carry:  # 任一链未完或进位未消化都要继续（覆盖 5+5=10）
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        carry, digit = divmod(s, 10)  # 个位落新节点，十位当下一轮进位
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
// 解法一：按竖式从低位加到高位，虚头省掉首节点特判。
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0) : val(x), next(nullptr) {}
};

ListNode* read_list() {
    // ACM 读入建链表：先长度后节点值；空链当 0。
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
    while (l1 || l2 || carry) {  // 任一链未完或进位未消化都要继续（覆盖 5+5=10）
        int s = carry;
        if (l1) {
            s += l1->val;
            l1 = l1->next;
        }
        if (l2) {
            s += l2->val;
            l2 = l2->next;
        }
        carry = s / 10;  // 个位落新节点，十位当下一轮进位
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

