## 思路

本题常见有三种写法。面试先讲推荐解，再补备选。

### 解法一：递归 DFS（推荐）
- 中序就是「左子树 → 根 → 右子树」，递归按这个顺序收集节点值即可。
- 空节点是递归终点，什么都不做，自然跳过缺失的子树。
- 先完整走完左子树再访问根；若是 BST 则输出递增，本题不要求是 BST，但顺序定义相同。
- 模板即此写法：代码最短，面试先画递归树再写。

### 解法二：显式栈迭代
- 一路沿左孩子压栈，直到没有左孩子；弹出时访问该节点，再转向它的右子树。
- 与解法一的调用栈展开完全等价，只是自己维护栈，避免语言递归深度限制。
- 时间仍 O(n)，空间 O(h)；链状树最坏 O(n)。
- 要求「不用递归」或手写迭代器时用这个。

### 解法三：Morris 中序
- 把当前节点左子树的最右节点（前驱）的右指针临时接到自己，走完左子树后再拆掉。
- 不需要栈或递归，额外空间 O(1)；每个节点的右指针最多被改两次，时间仍 O(n)。
- 会暂时改树，写完必须还原；并发或树只读时不能用。
- 面试加分项，不是第一选择。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)（递归栈；最坏链状 O(n)）
- 解法二：时间 O(n)，空间 O(h)（显式栈；最坏 O(n)）
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：递归中序，按「左 → 根 → 右」收集。
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
    # ACM 读入建树：层序 tokens，null 表示空孩子。下面 inorder 才是算法。
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


def inorder(root):
    ans = []

    def dfs(node):
        if node is None:
            return  # 空节点是递归终点
        dfs(node.left)
        ans.append(node.val)
        dfs(node.right)

    dfs(root)
    return ans


def main():
    vals = inorder(read_tree())
    if vals:
        print(" ".join(map(str, vals)))


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：递归中序，按「左 → 根 → 右」收集。
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* read_tree() {
    // ACM 读入建树：层序 tokens，null 表示空孩子。下面 inorder 才是算法。
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

void inorder(TreeNode* node, vector<int>& ans) {
    if (!node) return;  // 空节点是递归终点
    inorder(node->left, ans);
    ans.push_back(node->val);
    inorder(node->right, ans);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    vector<int> ans;
    inorder(root, ans);
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    if (!ans.empty()) cout << '\n';
    return 0;
}
```
