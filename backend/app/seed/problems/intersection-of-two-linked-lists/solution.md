## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：双指针换头（推荐）

- 相交后两条链共用同一段后缀，把两条链首尾相接走，路程差会被对消。
- 指针 `a` 走完 A 接到 B 头，`b` 走完 B 接到 A 头：若相交，第二次遍历时会在同一节点相遇。
- 不相交时两人最终都走到空，同样在 `None` 处相遇，正好对应「无交点」。
- 不需要先量长度再对齐：换头走等价于各补上对方的前缀长度。
- 比较的是节点身份（同一对象），不是节点值。

### 解法二：先量长度再对齐

- 先走完两条链得到长度，让长的那条先走出长度差，再同步前进。
- 第一次碰上的同一节点就是交点；同时走到空则不相交。
- 与解法一等价，多一次预先计数，画图更好讲，现场代码稍长。

### 解法三：哈希表记节点

- 把 A 的所有节点放进集合，再扫 B，第一个在集合里的就是交点。
- 时间线性，但要 O(nA) 额外空间，链表题通常要求 O(1) 空间。
- 同样必须用节点身份做键，值相等不算相交。

## 复杂度

- 解法一：时间 O(nA + nB)，空间 O(1)（不计建表）
- 解法二：时间 O(nA + nB)，空间 O(1)
- 解法三：时间 O(nA + nB)，空间 O(nA)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def read_vals(lines, i):
    n = int(lines[i].strip())
    i += 1
    if n == 0:
        return [], i
    return list(map(int, lines[i].split())), i + 1


def build(vals):
    dummy = ListNode()
    cur = dummy
    nodes = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    return dummy.next, nodes


def main():
    lines = sys.stdin.read().splitlines()
    i = 0
    vals_a, i = read_vals(lines, i)
    vals_b, i = read_vals(lines, i)
    skip_a, skip_b = map(int, lines[i].split())

    head_a, nodes_a = build(vals_a)
    if skip_a < 0:
        head_b, _ = build(vals_b)
    else:
        dummy = ListNode()
        cur = dummy
        for j in range(skip_b):
            cur.next = ListNode(vals_b[j])
            cur = cur.next
        cur.next = nodes_a[skip_a]
        head_b = dummy.next

    a, b = head_a, head_b
    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a
    print(-1 if a is None else a.val)


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

vector<int> read_vals() {
    int n;
    cin >> n;
    vector<int> vals(n);
    for (int i = 0; i < n; i++) cin >> vals[i];
    return vals;
}

pair<ListNode*, vector<ListNode*>> build(const vector<int>& vals) {
    ListNode dummy(0);
    ListNode* cur = &dummy;
    vector<ListNode*> nodes;
    for (int v : vals) {
        cur->next = new ListNode(v);
        cur = cur->next;
        nodes.push_back(cur);
    }
    return {dummy.next, nodes};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    vector<int> vals_a = read_vals();
    vector<int> vals_b = read_vals();
    int skip_a, skip_b;
    cin >> skip_a >> skip_b;

    auto [head_a, nodes_a] = build(vals_a);
    ListNode* head_b;
    if (skip_a < 0) {
        head_b = build(vals_b).first;
    } else {
        ListNode dummy(0);
        ListNode* cur = &dummy;
        for (int j = 0; j < skip_b; j++) {
            cur->next = new ListNode(vals_b[j]);
            cur = cur->next;
        }
        cur->next = nodes_a[skip_a];
        head_b = dummy.next;
    }

    ListNode *a = head_a, *b = head_b;
    while (a != b) {
        a = a ? a->next : head_b;
        b = b ? b->next : head_a;
    }
    if (!a) cout << -1 << "\n";
    else cout << a->val << "\n";
    return 0;
}
```
