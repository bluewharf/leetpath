## 思路

### 解法一：后序递归（推荐）

- 空树深度为 0；非空则深度 = `1 + max(左子树深度, 右子树深度)`。
- 这一定义正好是「根到最远叶子的节点数」，先算子树再汇总。
- 叶子左右都为空，返回 1；单链退化时答案等于节点数。
- 节点少时递归更短、更好背；和 BFS 差在用调用栈做「子树归约」，而不是按层计数。

### 解法二：层序 BFS

- 队列按层弹出，每处理完一层 `depth + 1`，结束时 `depth` 即最大深度。
- 空间最坏 O(n)（满二叉树最后一层），但链式树不会把递归栈打到 O(n)。
- 空树直接 0；和递归同一遍访问，只是深度来自层号而不是返回值。

### 解法三：迭代 DFS

- 栈内存 `(节点, 当前深度)`，弹出时刷新全局最大，再把子节点以 `depth+1` 入栈。
- 与递归等价，只是手动维护栈，适合限制递归深度的环境。
- 空间仍是 O(h)，最坏单链 O(n)。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)（h 为树高，递归栈）
- 解法二：时间 O(n)，空间 O(w)（w 为最大层宽，最坏 O(n)）
- 解法三：时间 O(n)，空间 O(h)

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


def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def main():
    print(max_depth(read_tree()))


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

int max_depth(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(max_depth(root->left), max_depth(root->right));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << max_depth(read_tree()) << "\n";
    return 0;
}
```
