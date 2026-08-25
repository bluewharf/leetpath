## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：后序 DFS 拆拐点路径与单向贡献（推荐）
- 每个节点问两件事：经过自己的最优路径和用来更新全局；能交给父节点的单向贡献只能选一侧。
- 子树贡献若为负就当 0 丢掉：走那条边只会更差，路径可以在本节点停住。
- 经过 `u` 的最大路径 = `u.val + max(0, L) + max(0, R)`，左右都能用，因为它自己就是拐点。
- 返回给父节点的是 `u.val + max(0, L, R)`：只能续一条链，否则到父节点会分叉，不再是路径。
- 全局初值取极小，全是负数时落到「只选一个最大节点」。模板即此写法。

### 解法二：枚举拐点再算左右最大链
- 对每个节点当拐点，再分别向下求「从该点出发的最大下行链」，拼成 `val + leftChain + rightChain`。
- 若不记忆化，每个拐点都重算子树，时间退化到 O(n²)；记忆化之后和一次后序等价。
- 思路好讲（「直径那题把边数换成权值和」），但实现比解法一啰嗦，还容易漏负权截断。
- 只适合口头拆问题；写代码仍用解法一一次走完。

## 复杂度

- 解法一：时间 O(n)，空间 O(h)（h 为树高，递归栈）
- 解法二：时间 O(n²)（朴素）或 O(n)（记忆化后），空间 O(h)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：后序 DFS。经过本节点的路径可左右都用；交给父节点只能续一侧。
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
    # ACM 读入建树：层序 tokens，null 表示空孩子。下面 dfs 才是算法。
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


def max_path_sum(root):
    ans = -10**18  # 全是负数时落到「只选一个最大节点」

    def dfs(node):
        nonlocal ans
        if not node:
            return 0
        left = max(dfs(node.left), 0)  # 负贡献丢掉：走那条边只会更差
        right = max(dfs(node.right), 0)
        ans = max(ans, node.val + left + right)  # 本节点当拐点，左右都能用
        return node.val + max(left, right)  # 交给父节点只能续一条链

    dfs(root)
    return ans


def main():
    print(max_path_sum(read_tree()))


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：后序 DFS。经过本节点的路径可左右都用；交给父节点只能续一侧。
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* read_tree() {
    // ACM 读入建树：层序 tokens，null 表示空孩子。下面 dfs 才是算法。
    int n;
    if (!(cin >> n) || n == 0) return nullptr;
    vector<string> tokens(n);
    for (int i = 0; i < n; ++i) cin >> tokens[i];
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
            ++i;
        }
        if (i < n) {
            node->right = parse(i);
            if (node->right) q.push(node->right);
            ++i;
        }
    }
    return root;
}

long long best_path = -(1LL << 60);  // 全是负数时落到「只选一个最大节点」

int dfs(TreeNode* node) {
    if (!node) return 0;
    int left = max(dfs(node->left), 0);  // 负贡献丢掉：走那条边只会更差
    int right = max(dfs(node->right), 0);
    best_path = max(best_path, (long long)node->val + left + right);  // 本节点当拐点
    return node->val + max(left, right);  // 交给父节点只能续一条链
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    TreeNode* root = read_tree();
    dfs(root);
    cout << best_path << '\n';
    return 0;
}
```
