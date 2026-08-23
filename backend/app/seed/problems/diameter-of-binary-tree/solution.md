## 思路

- 直径是任意两点路径的边数最大值，等于所有节点「左子树高度 + 右子树高度」的全局最大。
- 一次后序 DFS：先算左右高度，用二者之和更新答案，再返回本节点高度。
- 高度定义：空节点为 0，非空为 `1 + max(左高, 右高)`。
- 最长路径不一定过根，所以每个节点都要更新全局值。
- 空树和单节点没有边，直径为 0。

## 复杂度

- 时间：O(n)
- 空间：O(h)，h 为树高

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


def diameter(root):
    ans = 0

    def height(node):
        nonlocal ans
        if node is None:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        ans = max(ans, lh + rh)
        return 1 + max(lh, rh)

    height(root)
    return ans


def main():
    print(diameter(read_tree()))


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
    for (int i = 0; i < n; i++) cin >> tokens[i];
    auto parse = [&](int i) -> TreeNode* {
        if (tokens[i] == "null") return nullptr;
        return new TreeNode(stoi(tokens[i]));
    };
    TreeNode* root = parse(0);
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            node->left = parse(i);
            if (node->left) q.push(node->left);
            i++;
        }
        if (i < n) {
            node->right = parse(i);
            if (node->right) q.push(node->right);
            i++;
        }
    }
    return root;
}

int diameter(TreeNode* root) {
    int ans = 0;
    function<int(TreeNode*)> height = [&](TreeNode* node) -> int {
        if (!node) return 0;
        int lh = height(node->left);
        int rh = height(node->right);
        ans = max(ans, lh + rh);
        return 1 + max(lh, rh);
    };
    height(root);
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << diameter(read_tree()) << "\n";
    return 0;
}
```
