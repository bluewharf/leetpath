## 思路

### 解法一（推荐）：带上下界 DFS

- 有效 BST 不只是「左孩子 < 根 < 右孩子」，而是整棵左子树都严格小于根、整棵右子树都严格大于根。
- 递归时带开区间 `(lo, hi)`：当前节点必须落在这个区间里，再把右界收成自己传给左子树、左界收成自己传给右子树。
- 相等非法，所以比较是严格的 `<` / `>`；节点值可到 32 位整数两端，区间边界要用更大的类型（或 ±inf）。
- 空树 / 空子树视为合法，递归在空结点处返回 true。
- 一次 DFS 就能抓住「右子树里掺了个过小的节点」，不必等到中序才发现。

### 解法二：中序递归，记录前驱

- BST 的中序序列必须严格递增：访问当前结点前，它必须大于上一个被访问的值。
- 用一个可变的 `prev`（或返回当前子树最大值）贯穿整次中序。
- 与解法一差在：不显式传区间，而是靠「中序有序」这一 BST 充要条件；忘了严格递增（允许相等）就会漏。

### 解法三：中序迭代栈

- 用栈模拟中序：一路向左压栈，弹出时与前驱比较，再转向右子树。
- 不变量与解法二相同，只是改成迭代，避免最坏链状树把递归栈打满。
- 实现比带上下界 DFS 啰嗦，适合已经写过迭代中序的场合。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)，h 为树高（递归栈）
- 解法二：时间 O(n)，空间 O(h)
- 解法三：时间 O(n)，空间 O(h)

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
    # 建树：层序 token，与 BST 判定分开
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


def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    # 空子树合法；节点必须落在开区间 (low, high)
    if root is None:
        return True
    if not (low < root.val < high):
        return False  # 相等也非法；±inf 覆盖 32 位端点
    # 左子树右界收成自己，右子树左界收成自己
    return is_valid_bst(root.left, low, root.val) and is_valid_bst(
        root.right, root.val, high
    )


def main():
    root = read_tree()
    print("true" if is_valid_bst(root) else "false")


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
    // 建树：层序 token，与 BST 判定分开
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; i++) cin >> tokens[i];
    TreeNode* root = new TreeNode(stoi(tokens[0]));
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            string t = tokens[i++];
            if (t != "null") {
                node->left = new TreeNode(stoi(t));
                q.push(node->left);
            }
        }
        if (i < n) {
            string t = tokens[i++];
            if (t != "null") {
                node->right = new TreeNode(stoi(t));
                q.push(node->right);
            }
        }
    }
    return root;
}

bool isValidBST(TreeNode* node, long long lo, long long hi) {
    if (!node) return true;
    // 开区间：相等非法；long long 避免根为 INT_MIN/MAX 时边界溢出
    if (!(lo < node->val && node->val < hi)) return false;
    return isValidBST(node->left, lo, node->val) &&
           isValidBST(node->right, node->val, hi);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = readTree();
    cout << (isValidBST(root, LLONG_MIN, LLONG_MAX) ? "true" : "false") << "\n";
    return 0;
}
```
