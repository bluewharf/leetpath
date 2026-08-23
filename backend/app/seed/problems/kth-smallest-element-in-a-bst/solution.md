## 思路

- BST 的中序遍历就是升序，走到第 k 个弹出的节点就是答案。
- 用栈模拟：一路向左压栈，弹出时访问，再转向右子树，不必先收集整段序列。
- 每弹出一个节点 `k--`，减到 0 立刻返回，后面的节点不用看。
- 节点值互不相同，不存在「第 k 小对应多个节点」的歧义。
- 迭代写法避免递归深度随树高（最坏链状）炸掉，空间仍是 O(h)。

## 复杂度

- 时间：O(h + k)，最坏 O(n)
- 空间：O(h)

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


def build_tree(tokens):
    if not tokens or tokens[0] == "null":
        return None
    root = TreeNode(int(tokens[0]))
    q = deque([root])
    i = 1
    while q and i < len(tokens):
        node = q.popleft()
        if i < len(tokens):
            t = tokens[i]
            i += 1
            if t != "null":
                node.left = TreeNode(int(t))
                q.append(node.left)
        if i < len(tokens):
            t = tokens[i]
            i += 1
            if t != "null":
                node.right = TreeNode(int(t))
                q.append(node.right)
    return root


def kth_smallest(root, k):
    stack = []
    cur = root
    while True:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    tokens = data[1 : 1 + n] if n else []
    k = int(data[1 + n])
    print(kth_smallest(build_tree(tokens), k))


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

TreeNode* build_tree(const vector<string>& tokens) {
    if (tokens.empty() || tokens[0] == "null") return nullptr;
    TreeNode* root = new TreeNode(stoi(tokens[0]));
    queue<TreeNode*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < tokens.size()) {
        TreeNode* node = q.front();
        q.pop();
        if (i < tokens.size()) {
            const string& t = tokens[i++];
            if (t != "null") {
                node->left = new TreeNode(stoi(t));
                q.push(node->left);
            }
        }
        if (i < tokens.size()) {
            const string& t = tokens[i++];
            if (t != "null") {
                node->right = new TreeNode(stoi(t));
                q.push(node->right);
            }
        }
    }
    return root;
}

int kth_smallest(TreeNode* root, int k) {
    vector<TreeNode*> stack;
    TreeNode* cur = root;
    while (true) {
        while (cur) {
            stack.push_back(cur);
            cur = cur->left;
        }
        cur = stack.back();
        stack.pop_back();
        if (--k == 0) return cur->val;
        cur = cur->right;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    int k;
    cin >> k;
    cout << kth_smallest(build_tree(tokens), k) << "\n";
    return 0;
}
```
