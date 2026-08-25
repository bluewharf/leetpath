## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：递归交换（推荐）

- 翻转整棵树 = 每个节点都交换左右孩子，再对两棵子树各自翻转。
- 先交换再递归，或先递归再交换，结果相同；注意 C++ 里不要边赋值边递归，否则会把刚换过来的孩子再翻一次。
- 空节点是递归终点，单节点左右都空，交换无副作用。
- 层序输出时要把内部空位写成 `null`，但末尾连续 `null` 必须丢掉，否则和题面序列化约定对不上。

### 解法二：迭代 BFS / 栈

- 队列层序或显式栈 DFS：弹出一个节点就交换左右孩子，非空孩子入队/入栈。
- 每个节点仍只处理一次，结果与递归相同。
- 空间变成队列宽度或栈深度，最坏仍 O(n)；偏斜树时 BFS 不必担心递归爆栈。
- 空树直接返回，循环体不会跑。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)
- 解法二：时间 O(n)，空间 O(n)（队列最宽一层）或 O(h)（栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
    # 层序建树：n=0 为空；只把非 null 节点入队
    data = sys.stdin.read().split()
    n = int(data[0])
    if n == 0:
        return None
    tokens = data[1 : 1 + n]

    def parse(i):
        if tokens[i] == "null":
            return None
        return TreeNode(int(tokens[i]))

    root = parse(0)
    q = deque([root])
    i = 1
    while q and i < n:
        node = q.popleft()
        if i < n:
            node.left = parse(i)
            if node.left:
                q.append(node.left)
            i += 1
        if i < n:
            node.right = parse(i)
            if node.right:
                q.append(node.right)
            i += 1
    return root


def write_tree(root):
    # 层序输出：内部空位保留 null，末尾连续 null 丢掉
    if root is None:
        print(0)
        return
    tokens = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            tokens.append("null")
        else:
            tokens.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    print(len(tokens))
    print(" ".join(tokens))


def invert(root):
    # 先交换左右再递归子树；空节点直接返回
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert(root.left)
    invert(root.right)
    return root


def main():
    write_tree(invert(read_tree()))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* parse(const string& s) {
    if (s == "null") return nullptr;
    return new TreeNode(stoi(s));
}

TreeNode* read_tree() {
    // 层序建树：n=0 为空；只把非 null 节点入队
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    TreeNode* root = parse(tokens[0]);
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            node->left = parse(tokens[i++]);
            if (node->left) q.push(node->left);
        }
        if (i < n) {
            node->right = parse(tokens[i++]);
            if (node->right) q.push(node->right);
        }
    }
    return root;
}

void write_tree(TreeNode* root) {
    // 层序输出：内部空位保留 null，末尾连续 null 丢掉
    if (!root) {
        cout << 0 << "\n";
        return;
    }
    vector<string> tokens;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        if (!node) {
            tokens.push_back("null");
        } else {
            tokens.push_back(to_string(node->val));
            q.push(node->left);
            q.push(node->right);
        }
    }
    while (!tokens.empty() && tokens.back() == "null") tokens.pop_back();
    cout << tokens.size() << "\n";
    for (size_t i = 0; i < tokens.size(); i++) {
        if (i) cout << " ";
        cout << tokens[i];
    }
    cout << "\n";
}

TreeNode* invert(TreeNode* root) {
    // 先交换左右再递归子树；空节点直接返回
    if (!root) return nullptr;
    swap(root->left, root->right);
    invert(root->left);
    invert(root->right);
    return root;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    write_tree(invert(read_tree()));
    return 0;
}
```
