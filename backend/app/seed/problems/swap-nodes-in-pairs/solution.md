## 思路

- 考点是「改指针、不改值」：用 dummy 钉住新头，每次把相邻的 `a、b` 四条边重接成 `prev → b → a → 后续`。
- 交换前记下 `a = prev.next`、`b = a.next`，再按 `prev.next = b`、`a.next = b.next`、`b.next = a` 的顺序改，避免丢链。
- 一对交换完后，`prev` 落到 `a`（现在是这对的尾），下一轮从这里继续，保证相邻对互不 overlapping。
- 循环条件是 `prev.next` 与 `prev.next.next` 都在：奇数长度时最后一个节点自然留在原位。
- dummy 让头结点交换与中间交换走同一套代码，不必特判。

## 复杂度

- 时间：O(n)
- 空间：O(1)（迭代，只用常数指针）

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


def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        prev.next = b
        a.next = b.next
        b.next = a
        prev = a
    return dummy.next


def main():
    write_list(swap_pairs(read_list()))


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
    ListNode(int x = 0, ListNode* nxt = nullptr) : val(x), next(nxt) {}
};

ListNode* readList() {
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
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

void writeList(ListNode* head) {
    vector<int> vals;
    while (head) {
        vals.push_back(head->val);
        head = head->next;
    }
    cout << vals.size() << "\n";
    if (!vals.empty()) {
        for (size_t i = 0; i < vals.size(); i++) {
            if (i) cout << " ";
            cout << vals[i];
        }
        cout << "\n";
    }
}

ListNode* swapPairs(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    while (prev->next && prev->next->next) {
        ListNode* a = prev->next;
        ListNode* b = a->next;
        prev->next = b;
        a->next = b->next;
        b->next = a;
        prev = a;
    }
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    writeList(swapPairs(readList()));
    return 0;
}
```
