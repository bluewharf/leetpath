## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：字典树（推荐）

- 前缀树：每个节点挂一棵「字符 → 子节点」的映射，并打一个「是否成词」标记。
- insert 沿字符建缺失的边，走完把终点标成词；公共前缀自动共享同一条路径。
- search 必须走完全部字符且终点带成词标记；startsWith 只需路径存在。
- 查询失败就是中途缺边，不必回头。
- Python 用哈希孩子、C++ 用 `children[26]`，时间只跟单词长度有关，和已插入单词总数解耦。

### 解法二：哈希集合模拟

- 一个 set 存完整单词，另一个 set 存所有前缀；insert 时把每个前缀都丢进去。
- search / startsWith 变成集合查询，实现短，但不展示前缀共享，空间按「前缀字符串」计更浪费。
- 面试会被追问「真正的 Trie 怎么建」，所以只能当保底，模板必须写树。

## 复杂度

- 解法一：时间所有操作合计 O(总字符数)，空间 O(总字符数)
- 解法二：时间合计 O(总字符数)，空间 O(前缀条数 × 平均长度)，通常更大

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None


def main():
    q = int(sys.stdin.readline())
    trie = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "Trie":
            trie = Trie()
            print("null")
        elif op == "insert":
            trie.insert(parts[1])
            print("null")
        elif op == "search":
            print("true" if trie.search(parts[1]) else "false")
        elif op == "startsWith":
            print("true" if trie.startsWith(parts[1]) else "false")


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TrieNode {
    TrieNode* children[26]{};
    bool is_end = false;
};

class Trie {
    TrieNode* root;

public:
    Trie() : root(new TrieNode()) {}

    void insert(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            int k = ch - 'a';
            if (!node->children[k]) node->children[k] = new TrieNode();
            node = node->children[k];
        }
        node->is_end = true;
    }

    TrieNode* walk(const string& s) {
        TrieNode* node = root;
        for (char ch : s) {
            int k = ch - 'a';
            if (!node->children[k]) return nullptr;
            node = node->children[k];
        }
        return node;
    }

    bool search(const string& word) {
        TrieNode* node = walk(word);
        return node && node->is_end;
    }

    bool startsWith(const string& prefix) { return walk(prefix) != nullptr; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    Trie trie;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "Trie") {
            cout << "null\n";
        } else if (op == "insert") {
            string word;
            cin >> word;
            trie.insert(word);
            cout << "null\n";
        } else if (op == "search") {
            string word;
            cin >> word;
            cout << (trie.search(word) ? "true" : "false") << "\n";
        } else if (op == "startsWith") {
            string prefix;
            cin >> prefix;
            cout << (trie.startsWith(prefix) ? "true" : "false") << "\n";
        }
    }
    return 0;
}
```
