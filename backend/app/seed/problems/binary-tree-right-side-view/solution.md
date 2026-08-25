## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：层序 BFS 取每层最后一个（推荐）
- 右侧能看到的，就是每一层最靠右的那个节点。
- 先左后右入队，进入一层前记下 `size`，下标 `i == size-1` 的那个就是该层最右。
- 空树队列为空，不输出；结果按层从上到下排好。
- 模板即此写法，和层序遍历只差「每层只留一个值」。

### 解法二：DFS 先右后左
- 带深度递归：先访问右子树再左子树，每个深度第一次走到的节点就是该层最右。
- 用 `len(ans) == depth` 判断这一层还没有记录过。
- 时间 O(n)，空间是递归栈 O(h)，不必同时存整层。
- 树很宽时比 BFS 省队列；要求「不用队列」或顺手写 DFS 时用。面试默认可先讲解法一。

## 复杂度

- 解法一：时间 O(n)，空间 O(w)（w 为最大层宽，最坏 O(n)）
- 解法二：时间 O(n)，空间 O(h)（递归栈；不计答案）

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


def main():
    root = read_tree()
    if root is None:
        return
    ans = []
    q = deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                ans.append(str(node.val))
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    print(" ".join(ans))


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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    if (!root) return 0;
    vector<int> ans;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = (int)q.size();
        for (int i = 0; i < sz; ++i) {
            TreeNode* node = q.front();
            q.pop();
            if (i == sz - 1) ans.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    if (!ans.empty()) cout << '\n';
    return 0;
}
```
