## 思路

- 中序就是「左子树 → 根 → 右子树」，递归按这个顺序收集节点值即可。
- 空节点是递归终点，什么都不做，自然跳过缺失的子树。
- 先完整走完左子树再访问根，保证输出序列与 BST 中从小到大的顺序一致（本题不要求是 BST，但顺序定义相同）。
- 也可用栈：一路向左压栈，弹出时访问再转向右子树，与递归展开等价。

## 复杂度

- 时间：O(n)（每个节点进出一次）
- 空间：O(h)，h 为树高（递归栈 / 显式栈；最坏链状 O(n)）

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


def inorder(root):
    ans = []

    def dfs(node):
        if node is None:
            return
        dfs(node.left)
        ans.append(node.val)
        dfs(node.right)

    dfs(root)
    return ans


def main():
    vals = inorder(read_tree())
    if vals:
        print(" ".join(map(str, vals)))


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

TreeNode* read_tree() {
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; ++i) cin >> tokens[i];
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
            ++i;
        }
        if (i < n) {
            if (tokens[i] != "null") {
                node->right = new TreeNode(stoi(tokens[i]));
                q.push(node->right);
            }
            ++i;
        }
    }
    return root;
}

void inorder(TreeNode* node, vector<int>& ans) {
    if (!node) return;
    inorder(node->left, ans);
    ans.push_back(node->val);
    inorder(node->right, ans);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    vector<int> ans;
    inorder(root, ans);
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    if (!ans.empty()) cout << '\n';
    return 0;
}
```
