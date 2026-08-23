## 思路

- 哈希表 + 双向链表：哈希 O(1) 定位节点，链表 O(1) 调整「最近使用」顺序。
- 链表一端是最久未使用，另一端是刚刚访问过；`get` / `put` 命中都把该节点移到最近端。
- `put` 新键时先插入最近端，键数超过容量再从最久端删一个。
- 对已有键再 `put` 只更新值并视为一次使用，容量不变。
- Python 可用 `OrderedDict`（`move_to_end` / `popitem(last=False)`）等价实现同一套语义。

## 复杂度

- 时间：每次 `get`/`put` 平均 O(1)
- 空间：O(capacity)

## 模板代码

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
