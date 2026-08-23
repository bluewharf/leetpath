## 思路

- 一棵树对称，当且仅当根的左子树与右子树互为镜像，不必再和根比。
- 镜像判定：对应节点值相等，并且「A 的左」对「B 的右」、「A 的右」对「B 的左」继续镜像。
- 一边空一边不空直接失败；两边都空才算这一层匹配（`a is b`）。
- 空树没有左右可比较，约定为对称。
- 递归把「整棵树是否对称」拆成「两棵子树是否镜像」，结构与层序无关。

## 复杂度

- 时间：O(n)
- 空间：O(h)，h 为树高（递归栈）

## 模板代码

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
    n = int(sys.stdin.readline())
    if n == 0:
        return None
    tokens = sys.stdin.readline().split()

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


def is_symmetric(root):
    def mirror(a, b):
        if a is None or b is None:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return root is None or mirror(root.left, root.right)


def main():
    print("true" if is_symmetric(read_tree()) else "false")


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

TreeNode* readTree() {
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    auto parse = [&](int i) -> TreeNode* {
        if (tokens[i] == "null") return nullptr;
        return new TreeNode(stoi(tokens[i]));
    };
    TreeNode* root = parse(0);
    if (!root) return nullptr;
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            node->left = parse(i++);
            if (node->left) q.push(node->left);
        }
        if (i < n) {
            node->right = parse(i++);
            if (node->right) q.push(node->right);
        }
    }
    return root;
}

bool isMirror(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && isMirror(a->left, b->right) && isMirror(a->right, b->left);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = readTree();
    bool ok = !root || isMirror(root->left, root->right);
    cout << (ok ? "true" : "false") << "\n";
    return 0;
}
```
