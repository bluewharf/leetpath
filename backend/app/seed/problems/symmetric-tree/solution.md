## 思路

### 解法一（推荐）：递归判断镜像

- 一棵树对称，当且仅当根的左子树与右子树互为镜像，不必再和根比。
- 镜像判定：对应节点值相等，并且「A 的左」对「B 的右」、「A 的右」对「B 的左」继续镜像。
- 一边空一边不空直接失败；两边都空才算这一层匹配（`a is b`）。
- 空树没有左右可比较，约定为对称。
- 递归把「整棵树是否对称」拆成「两棵子树是否镜像」，结构与层序无关。

### 解法二：队列成对迭代

- 把 `(root.left, root.right)` 入队，每次弹出一对：都空则继续，一个空或值不等则失败。
- 再按「A 左 / B 右」「A 右 / B 左」的顺序入队，保证比较的是镜像位置。
- 与解法一同一不变量，只是把递归改成显式队列，最坏空间 O(n)（最宽一层）。

### 解法三：层序后检查每层回文

- BFS 按层收集结点值（空孩子用哨兵占位），判断该层序列是否回文。
- 必须保留空位，否则 `1 / 2,null` 与 `1 / null,2` 以外的不对称结构会被漏掉。
- 比成对比较啰嗦，且哨兵处理易错，一般只作思路对照。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)，h 为树高（递归栈）
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(n)

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
    # 建树：层序 token，null 为空，末尾连续 null 已省略
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


def is_symmetric(root):
    def mirror(a, b):
        # 一边空一边不空失败；两边都空（a is b）才算这一对匹配
        if a is None or b is None:
            return a is b
        # 镜像：值相等，且交叉比较左右
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    # 空树约定对称；只需左右子树互为镜像
    return root is None or mirror(root.left, root.right)


def main():
    print("true" if is_symmetric(read_tree()) else "false")


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

TreeNode* readTree() {
    // 建树：层序 token，与镜像判定分开
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    auto parse = [&](int i) -> TreeNode* {
        if (tokens[i] == "null") return nullptr;
        return new TreeNode(stoi(tokens[i]));
    };
    TreeNode* root = parse(0);
    if (!root) return nullptr;
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            node->left = parse(i++);
            if (node->left) q.push(node->left);
        }
        if (i < n) {
            node->right = parse(i++);
            if (node->right) q.push(node->right);
        }
    }
    return root;
}

bool isMirror(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;  // 都空才对称，一空一非空失败
    return a->val == b->val && isMirror(a->left, b->right) && isMirror(a->right, b->left);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = readTree();
    bool ok = !root || isMirror(root->left, root->right);  // 空树为真
    cout << (ok ? "true" : "false") << "\n";
    return 0;
}
```
