## 思路

两棵树同构：都空则真，一个空则假，值相等且左右子树分别相同。注意别写成镜像。

### 解法一（推荐）：同步递归

- 两个节点都空 → 相同；恰好一个空 → 不同；值不等 → 不同。
- 否则比较 `p.left` 对 `q.left`、`p.right` 对 `q.right`。
- 左右交换不算相同，不要交叉比较。

### 解法二：双队列 BFS

- 两个队列同步弹出，每次比较一对节点的空/不空和值，再按左、右顺序入队。
- 与递归同一不变量，只是自己维护队列。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)
- 解法二：时间 O(n)，空间 O(n)

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


def same(a, b):
    if a is None or b is None:
        return a is b
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


def main():
    p = read_tree()
    q = read_tree()
    print("true" if same(p, q) else "false")


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

bool same(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && same(a->left, b->left) && same(a->right, b->right);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* p = read_tree();
    TreeNode* q = read_tree();
    cout << (same(p, q) ? "true" : "false") << '\n';
    return 0;
}
```
