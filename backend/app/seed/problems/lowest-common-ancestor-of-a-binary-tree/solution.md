## 思路

- 后序递归：先在左右子树里找 `p`/`q`，再根据「哪边找到了」判断当前节点是不是 LCA。
- 当前节点就是 `p` 或 `q` 时直接返回——一个节点可以是自己的祖先。
- 左右都非空：两个目标分居两侧，当前节点就是最近公共祖先。
- 只有一侧非空：LCA 在那一侧继续向上传；两侧都空则返回空。
- 题目保证 `p`、`q` 都在树中且值互异，不必处理「找不到」的分支。

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
    line = sys.stdin.readline()
    if not line:
        return None
    n = int(line.strip())
    if n == 0:
        return None
    tokens = sys.stdin.readline().split()
    root = TreeNode(int(tokens[0]))
    q = deque([root])
    i = 1
    while q and i < n:
        node = q.popleft()
        if i < n:
            t = tokens[i]
            i += 1
            if t != "null":
                node.left = TreeNode(int(t))
                q.append(node.left)
        if i < n:
            t = tokens[i]
            i += 1
            if t != "null":
                node.right = TreeNode(int(t))
                q.append(node.right)
    return root


def lowest_common_ancestor(root, p, q):
    if root is None or root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root
    return left if left is not None else right


def main():
    root = read_tree()
    p, q = map(int, sys.stdin.readline().split())
    print(lowest_common_ancestor(root, p, q).val)


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
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* read_tree() {
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    TreeNode* root = new TreeNode(stoi(tokens[0]));
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            if (tokens[i] != "null") {
                node->left = new TreeNode(stoi(tokens[i]));
                q.push(node->left);
            }
            i++;
        }
        if (i < n) {
            if (tokens[i] != "null") {
                node->right = new TreeNode(stoi(tokens[i]));
                q.push(node->right);
            }
            i++;
        }
    }
    return root;
}

TreeNode* lca(TreeNode* root, int p, int q) {
    if (!root || root->val == p || root->val == q) return root;
    TreeNode* left = lca(root->left, p, q);
    TreeNode* right = lca(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    int p, q;
    cin >> p >> q;
    cout << lca(root, p, q)->val << "\n";
    return 0;
}
```
