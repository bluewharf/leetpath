## 思路

### 解法一（推荐）：dummy + 快慢指针一次遍历

- 一次遍历删除倒数第 k 个：快指针先走 k 步，再和慢指针一起走。
- 在头前加 dummy，快慢都从 dummy 出发；快指针走到尾时，慢指针恰好停在待删结点的前驱。
- 删头、删中间、删尾都走同一套 `slow.next = slow.next.next`，不用先数长度。
- 题目保证 k 合法，快指针先走 k 步不会落空。

### 解法二：先数长度再删

- 第一遍得到 `n`，倒数第 k 即正数第 `n-k+1`，第二遍走到前驱删除。
- 两次遍历，逻辑直白；空表/删头仍建议 dummy，避免单独写删头分支。
- 和快慢指针比：少了「间距为 k」的不变量，多一次完整扫描。

### 解法三：递归返回倒数序号

- 递归到 `null` 返回 0，回溯时序号加一，等于 k 时让父节点跳过自己。
- 空间 O(n)，写起来绕，且要处理删头（返回新头）。
- 适合口述「用栈从后往前数」，落地仍推解法一。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# —— 建表（I/O）：n 与结点值后跟 k；空表只读 n 与 k ——
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


# —— 算法：dummy + 快慢间距 k，fast 到尾时 slow 停在待删前驱 ——
def remove_nth(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)  # 哨兵让删头与删中间走同一套
    fast = dummy
    for _ in range(k):  # 题目保证 k 合法，先走 k 步不会落空
        fast = fast.next
    slow = dummy
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next


def main() -> None:
    head, k = read_list()
    write_list(remove_nth(head, k))


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

// —— 建表（I/O）：n 与结点值后跟 k；空表只读 n 与 k ——
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

// —— 算法：dummy + 快慢间距 k，fast 到尾时 slow 停在待删前驱 ——
ListNode* remove_nth(ListNode* head, int k) {
    ListNode dummy(0, head);  // 哨兵让删头与删中间走同一套
    ListNode* fast = &dummy;
    for (int i = 0; i < k; i++) fast = fast->next;  // k 合法，先走 k 步不会落空
    ListNode* slow = &dummy;
    while (fast->next) {
        slow = slow->next;
        fast = fast->next;
    }
    slow->next = slow->next->next;
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    ListNode* head = read_list(k);
    write_list(remove_nth(head, k));
    return 0;
}
```
