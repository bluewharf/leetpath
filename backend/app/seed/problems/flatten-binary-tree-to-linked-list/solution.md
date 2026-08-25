## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：倒序先序递归（推荐）

- 先序展开：根、左、右，改成「右指针串后继、左指针全空」的单链。
- 倒着做：先递归右子树再递归左子树，用 `prev` 记住已经串好的先序后继。
- 回溯时把当前节点的右指针接到 `prev`、左指针置空，再把 `prev` 更新为当前节点。
- 这样按先序的逆序把节点逐个接到链头，结束后 `prev` 正好停在根。
- 不必先切下左右子树再拼接，一次后序改指针即可原地完成。

### 解法二：先递归再拼接

- 正向：先把左右子树各自摊平，记下左链的尾巴，再 `根 → 左链 → 右链`。
- 递归返回前要保留右子树指针，否则左链接上去之后右子树就丢了。
- 与解法一生成同一条先序链，只是「子树内部先摊好再接」，空间同样是递归栈。

### 解法三：迭代找前驱

- 若当前节点有左子树：找到左子树最右节点（先序前驱），把它的右指针接到原右子树，再把左子树挪到右边、左指针置空。
- 然后沿右指针走到下一个节点继续，整棵树被摊成右链。
- 不额外开栈，空间 O(1)，是解法一的迭代对照。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)（递归栈）
- 解法二：时间 O(n)，空间 O(h)
- 解法三：时间 O(n)，空间 O(1)

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


def write_tree(root):
    if root is None:
        print(0)
        return
    tokens = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            tokens.append("null")
            continue
        tokens.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    print(len(tokens))
    print(" ".join(tokens))


def flatten(root):
    prev = None

    def dfs(node):
        nonlocal prev
        if not node:
            return
        dfs(node.right)
        dfs(node.left)
        node.right = prev
        node.left = None
        prev = node

    dfs(root)


def main():
    root = read_tree()
    flatten(root)
    write_tree(root)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
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

void write_tree(TreeNode* root) {
    if (!root) {
        cout << 0 << "\n";
        return;
    }
    vector<string> tokens;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        if (!node) {
            tokens.push_back("null");
            continue;
        }
        tokens.push_back(to_string(node->val));
        q.push(node->left);
        q.push(node->right);
    }
    while (!tokens.empty() && tokens.back() == "null") tokens.pop_back();
    cout << tokens.size() << "\n";
    for (size_t i = 0; i < tokens.size(); i++) {
        if (i) cout << " ";
        cout << tokens[i];
    }
    cout << "\n";
}

void flatten(TreeNode* root) {
    TreeNode* prev = nullptr;
    function<void(TreeNode*)> dfs = [&](TreeNode* node) {
        if (!node) return;
        dfs(node->right);
        dfs(node->left);
        node->right = prev;
        node->left = nullptr;
        prev = node;
    };
    dfs(root);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    flatten(root);
    write_tree(root);
    return 0;
}
```
