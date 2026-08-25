## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：BFS 按层出队（推荐）
- 层序就是 BFS：队列里始终是「当前要处理的一层」，弹出时把孩子排到队尾当下一层。
- 进入一层前记下 `size = 队列长度`，只处理这么多个节点，这一批就是同一层从左到右。
- 先左后右入队，同层顺序自然正确；空树队列为空，一层都不输出。
- 模板即此写法，和「右视图 / 锯齿层序」共用同一骨架。

### 解法二：DFS 按深度收集
- 先序递归，额外传 `depth`：第一次到达该深度就新建一层数组，然后把节点值追加进去。
- 仍先左后右，同层从左到右的顺序与 BFS 一致。
- 时间 O(n)，空间是递归栈 O(h) 加答案；不像 BFS 那样队列里同时堆着一整层。
- 树很宽、栈深可控时可用；题目要的就是层序，面试默认还是解法一。

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
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(str(node.val))
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        print(" ".join(level))


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
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = (int)q.size();
        for (int k = 0; k < sz; ++k) {
            TreeNode* node = q.front();
            q.pop();
            if (k) cout << ' ';
            cout << node->val;
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        cout << '\n';
    }
    return 0;
}
```
