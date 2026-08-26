## 思路

本题就是层序遍历加一层方向翻转。先把普通 BFS 写对，再处理奇数层。

### 解法一（推荐）：BFS 分层后翻转

- 队列按层取出 `size` 个节点，从左到右收集本层值，同时把左右孩子入队。
- 层号从 0 起：偶数层保持从左到右，奇数层把本层数组反转后再输出。
- 空树直接结束，不要输出空行。
- 和「层序遍历」只差这一次反转，面试先写对层序再加方向。

### 解法二：双端队列一头加

- 用 deque：偶数层从尾部弹出、孩子从左到右追加；奇数层从头部弹出、孩子从右到左插入头部。
- 不必事后 reverse，方向写进入队顺序。
- 实现细节比解法一多，容易把左右孩子顺序写反。

## 复杂度

- 解法一：时间 O(n)，空间 O(w)（w 为最宽一层）
- 解法二：时间 O(n)，空间 O(w)

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


def main():
    root = read_tree()
    if root is None:
        return
    q = deque([root])
    level_id = 0
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(str(node.val))
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        if level_id % 2 == 1:
            level.reverse()  # 奇数层从右到左
        print(" ".join(level))
        level_id += 1


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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    if (!root) return 0;
    queue<TreeNode*> q;
    q.push(root);
    int level_id = 0;
    while (!q.empty()) {
        int size = (int)q.size();
        vector<int> level;
        for (int i = 0; i < size; ++i) {
            TreeNode* node = q.front();
            q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        if (level_id % 2 == 1) reverse(level.begin(), level.end());  // 奇数层从右到左
        for (size_t i = 0; i < level.size(); ++i) {
            if (i) cout << ' ';
            cout << level[i];
        }
        cout << '\n';
        ++level_id;
    }
    return 0;
}
```
