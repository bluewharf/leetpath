## 思路

### 解法一（推荐）：迭代三指针

- 迭代三指针反转：`prev` / `cur` / `nxt`，把每条边的方向拧过来。
- 保存 `cur.next` 后，把 `cur.next` 改指 `prev`，再整体前移一格。
- 循环结束时 `prev` 就是新头；空链表、单结点自然正确。
- 不需要递归：迭代已经是 O(1) 额外空间的标准写法。

### 解法二：递归

- 先 `reverse(head.next)` 得到新头，再把后继指回自己、自己 `next` 置空。
- 语义是「后面先翻过来再接上自己」；空表/单结点作为递归出口。
- 空间 O(n)，长链可能爆栈，面试常作为迭代的对照。

### 解法三：dummy 头插

- 逐个把结点从原链摘下，插到 dummy 后面，相当于不断把当前结点变成新头。
- 与解法一本质相同，只是用哨兵表达「新链的头」，少一个名为 `prev` 的变量。
- 头插写乱时容易把 `nxt` 丢了，仍建议先掌握三指针。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# —— 建表（I/O）：第一行 n，随后 n 个值；空表输出单行 0 ——
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


def write_list(head: ListNode | None) -> None:
    vals: list[str] = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


# —— 算法：三指针迭代反转；结束时 prev 是新头 ——
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    cur = head
    while cur:
        nxt = cur.next  # 先保住后继，再把边拧向 prev
        cur.next = prev
        prev = cur
        cur = nxt
    return prev  # 空表/单结点自然正确


def main() -> None:
    write_list(reverse_list(read_list()))


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

// —— 建表（I/O）：第一行 n，随后 n 个值；空表输出单行 0 ——
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
    if (vals.empty()) {
        cout << 0 << '\n';
        return;
    }
    cout << vals.size() << '\n';
    for (size_t i = 0; i < vals.size(); i++) {
        if (i) cout << ' ';
        cout << vals[i];
    }
    cout << '\n';
}

// —— 算法：三指针迭代反转；结束时 prev 是新头 ——
ListNode* reverse_list(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* nxt = cur->next;  // 先保住后继，再把边拧向 prev
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;  // 空表/单结点自然正确
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    write_list(reverse_list(read_list()));
    return 0;
}
```
