## 思路

- Floyd 判圈：快指针一次两步、慢指针一次一步，有环则必在环内相遇。
- 无环时快指针先到末尾（`fast` 或 `fast.next` 为空），直接判 false。
- 相遇依据是节点对象相同，不是值相同；值重复的无环链不会误判。
- 空链表没有节点可走，直接 false。
- 空间 O(1)，不必用哈希表记访问过的节点。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

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
        print("false")
        return
    vals = list(map(int, data[1 : 1 + n]))
    pos = int(data[1 + n])
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
            print("true")
            return
    print("false")


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
        cout << "false\n";
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
    if (pos >= 0 && pos < n) nodes[n - 1]->next = nodes[pos];
    ListNode* slow = nodes[0];
    ListNode* fast = nodes[0];
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            cout << "true\n";
            return 0;
        }
    }
    cout << "false\n";
    return 0;
}
```
