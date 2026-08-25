## 思路

### 解法一：哈希表 + 双向链表（推荐）

- 哈希 O(1) 定位节点，双向链表 O(1) 调整「最近使用」顺序；一端 LRU，一端 MRU。
- `get` / `put` 命中都把该节点移到最近端；`put` 新键先插最近端，超容量再从最久端删一个。
- 对已有键再 `put` 只更新值并视为一次使用，容量不变。
- 模板里 Python 用 `OrderedDict`（`move_to_end` / `popitem(last=False)`），C++ 用 `list` + `unordered_map` 指向迭代器，语义同一套。
- 考的是「O(1) 删除任意位置」：单靠队列、栈或普通哈希做不到同时定位和改序。

### 解法二：手写 prev/next 节点

- 节点存 `key`、`value`、`prev`、`next`，外加哑头哑尾；哈希仍是 `key → 节点`。
- 移到链尾 = 先从原位置摘下，再接到哑尾之前；淘汰 = 删哑头之后第一个。
- 和语言自带链表同一复杂度，面试常要求当场写出节点结构，不依赖 `OrderedDict` / `list.splice`。

### 解法三：时间戳懒淘汰

- 每次访问给 key 打递增时间戳，淘汰时扫哈希或从堆里弹过期项。
- `get`/`put` 变成 O(capacity) 或均摊不是严格 O(1)，容量一大就会慢。
- 只适合讲清「为何必须双向链表」的反例，提交必须用解法一。

## 复杂度

- 解法一：每次 get/put 平均时间 O(1)，空间 O(capacity)
- 解法二：每次 get/put 时间 O(1)，空间 O(capacity)
- 解法三：每次 get/put 时间 O(capacity) 或均摊 O(log capacity)（堆），空间 O(capacity)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)


def main():
    q = int(sys.stdin.readline())
    cache = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "LRUCache":
            cache = LRUCache(int(parts[1]))
            print("null")
        elif op == "put":
            cache.put(int(parts[1]), int(parts[2]))
            print("null")
        elif op == "get":
            print(cache.get(int(parts[1])))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class LRUCache {
    int cap;
    list<pair<int, int>> lst;  // front = LRU, back = MRU
    unordered_map<int, list<pair<int, int>>::iterator> mp;

public:
    LRUCache(int capacity) : cap(capacity) {}

    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        lst.splice(lst.end(), lst, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = mp.find(key);
        if (it != mp.end()) {
            it->second->second = value;
            lst.splice(lst.end(), lst, it->second);
            return;
        }
        lst.emplace_back(key, value);
        mp[key] = prev(lst.end());
        if ((int)mp.size() > cap) {
            mp.erase(lst.front().first);
            lst.pop_front();
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    LRUCache* cache = nullptr;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "LRUCache") {
            int cap;
            cin >> cap;
            cache = new LRUCache(cap);
            cout << "null\n";
        } else if (op == "put") {
            int k, v;
            cin >> k >> v;
            cache->put(k, v);
            cout << "null\n";
        } else if (op == "get") {
            int k;
            cin >> k;
            cout << cache->get(k) << "\n";
        }
    }
    return 0;
}
```
