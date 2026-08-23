## 思路

- 每个节点问两件事：经过自己的「最优路径和」用来更新全局；能交给父节点的「单向贡献」只能选一侧。
- 子树贡献若为负就当 0 丢掉：走那条边只会更差，路径可以在本节点停住。
- 经过 `u` 的最大路径 = `u.val + max(0, L) + max(0, R)`，左右都能用，因为它自己就是拐点。
- 返回给父节点的是 `u.val + max(0, L, R)`：只能续一条链，否则到父节点会分叉，不再是路径。
- 全局初值取极小，这样全是负数时会落到「只选一个最大节点」。

## 复杂度

- 时间：O(n)（后序各走一遍）
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


def max_path_sum(root):
    ans = -10**18

    def dfs(node):
        nonlocal ans
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        ans = max(ans, node.val + left + right)
        return node.val + max(left, right)

    dfs(root)
    return ans


def main():
    print(max_path_sum(read_tree()))


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
            ++i;
        }
        if (i < n) {
            node->right = parse(i);
            if (node->right) q.push(node->right);
            ++i;
        }
    }
    return root;
}

long long best_path = -(1LL << 60);

int dfs(TreeNode* node) {
    if (!node) return 0;
    int left = max(dfs(node->left), 0);
    int right = max(dfs(node->right), 0);
    best_path = max(best_path, (long long)node->val + left + right);
    return node->val + max(left, right);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    dfs(root);
    cout << best_path << '\n';
    return 0;
}
```
