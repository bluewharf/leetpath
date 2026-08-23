## 思路

- 右侧能看到的，就是每一层最靠右的那个节点。
- 层序 BFS：先左后右入队，处理一层时最后一个弹出的就是该层最右。
- 等价写法：DFS 先右后左，每层第一次访问到的节点就是右视图。
- 空树没有任何层，不输出。

## 复杂度

- 时间：O(n)
- 空间：O(w)，w 为最大层宽（队列；最坏 O(n)）

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
