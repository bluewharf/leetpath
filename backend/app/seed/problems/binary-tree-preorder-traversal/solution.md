## 思路

前序是「根 → 左 → 右」。递归最直；迭代用栈时先压右再压左，才能先弹出左。

### 解法一（推荐）：递归 DFS

- 访问根，再递归左，再递归右。空节点直接返回。
- 和中序只差「打印时机」：前序进节点就收集，中序左子树走完再收集。

### 解法二：显式栈

- 根入栈。弹出即访问，然后先压右孩子再压左孩子，保证左先出。
- 要求「不要递归」时用这个。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)
- 解法二：时间 O(n)，空间 O(h)

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
    # ACM 读入建树：层序 tokens，null 表示空孩子。
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


def preorder(root):
    ans = []

    def dfs(node):
        if node is None:
            return
        ans.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return ans


def main():
    vals = preorder(read_tree())
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
    // ACM 读入建树：层序 tokens，null 表示空孩子。
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

void preorder(TreeNode* node, vector<int>& ans) {
    if (!node) return;
    ans.push_back(node->val);
    preorder(node->left, ans);
    preorder(node->right, ans);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    vector<int> ans;
    preorder(root, ans);
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    if (!ans.empty()) cout << '\n';
    return 0;
}
```
