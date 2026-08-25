## 思路

### 解法一：后序递归（推荐）

- 先在左右子树里找 `p`/`q`，再根据「哪边找到了」判断当前节点是不是 LCA。
- 当前节点就是 `p` 或 `q` 时直接返回——一个节点可以是自己的祖先。
- 左右都非空：两个目标分居两侧，当前节点就是最近公共祖先。
- 只有一侧非空：LCA 在那一侧继续向上传；两侧都空则返回空。
- 题目保证 `p`、`q` 都在树中且值互异，不必处理「找不到」；一次遍历把「两侧信息」压缩进返回值。

### 解法二：父指针 + 祖先集合

- 一遍 BFS/DFS 记下每个节点的父指针，从 `p` 沿父链把祖先放进集合，再从 `q` 往上走，第一个命中集合的就是 LCA。
- 显式构造「到根的路径」，好理解，但要额外哈希和父映射，空间 O(n)。
- 和后序递归比：把公共祖先从「返回值归约」改成「路径求交」。

### 解法三：分别记录到根路径

- 两次 DFS 分别记下 `root → p`、`root → q` 的节点序列，并排比较，最后一个相同节点即 LCA。
- 和父指针本质相同，只是用路径数组替代哈希集合。
- 本题节点值唯一，路径里存值即可；有重复值时必须存引用。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)（h 为树高，递归栈）
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(h)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：后序归约。左右都命中则当前为 LCA；节点可以是自己的祖先。
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
    # 层序建树：n=0 为空；只把非 null 节点入队。与 LCA 算法无关。
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
    # 算法：后序归约。空或命中 p/q 向上传（节点可以是自己的祖先）。
    if root is None or root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root  # 两目标分居两侧，当前就是 LCA
    return left if left is not None else right  # 都在同一侧，或都未找到


def main():
    root = read_tree()
    p, q = map(int, sys.stdin.readline().split())
    print(lowest_common_ancestor(root, p, q).val)


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：后序归约。左右都命中则当前为 LCA；节点可以是自己的祖先。
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* read_tree() {
    // 层序建树：n=0 为空；只把非 null 节点入队。与 LCA 算法无关。
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
    // 后序：左右都命中则当前为 LCA；只一侧非空则 LCA 在那一侧。
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
