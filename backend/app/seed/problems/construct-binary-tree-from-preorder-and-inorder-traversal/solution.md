## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：哈希定位 + 递归分治（推荐）
- 先序第一个元素必是当前子树的根，中序里这个根把左右子树切成两段。
- 值互不相同，先把中序「值 → 下标」放进哈希表，切分就是 O(1) 查表。
- 维护一个先序下标，每次递归取出下一个值当根；必须先递归左区间再右区间，才能和先序的「根-左-右」对齐。
- 中序闭区间为空则返回空节点。模板即此写法。
- 建完按层序序列化，末尾连续 `null` 丢掉，空树输出 `0`。

### 解法二：中序线性找根
- 不建哈希表，每次在中序区间里扫描根的位置再切开。
- 不变量与解法一相同，但每次切分是 O(区间长)，最坏链状树会到 O(n²)。
- 空间少一张哈希表，只剩递归栈 O(h)。
- n 到 3000 时链状可能吃紧；只有被追问「不许用哈希」才写这个，默认仍用解法一。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)（哈希表 + 递归栈）
- 解法二：时间 O(n²)，空间 O(h)

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


def build_tree(preorder, inorder):
    if not preorder:
        return None
    pos = {v: i for i, v in enumerate(inorder)}
    i = 0

    def helper(lo, hi):
        nonlocal i
        if lo > hi:
            return None
        val = preorder[i]
        i += 1
        node = TreeNode(val)
        mid = pos[val]
        node.left = helper(lo, mid - 1)
        node.right = helper(mid + 1, hi)
        return node

    return helper(0, len(inorder) - 1)


def serialize(root):
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


def main():
    n = int(sys.stdin.readline().strip())
    if n == 0:
        serialize(None)
        return
    preorder = list(map(int, sys.stdin.readline().split()))
    inorder = list(map(int, sys.stdin.readline().split()))
    serialize(build_tree(preorder, inorder))


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

TreeNode* build_tree(const vector<int>& preorder, const vector<int>& inorder) {
    if (preorder.empty()) return nullptr;
    unordered_map<int, int> pos;
    for (int i = 0; i < (int)inorder.size(); i++) pos[inorder[i]] = i;
    int i = 0;
    function<TreeNode*(int, int)> helper = [&](int lo, int hi) -> TreeNode* {
        if (lo > hi) return nullptr;
        int val = preorder[i++];
        TreeNode* node = new TreeNode(val);
        int mid = pos[val];
        node->left = helper(lo, mid - 1);
        node->right = helper(mid + 1, hi);
        return node;
    };
    return helper(0, (int)inorder.size() - 1);
}

void serialize(TreeNode* root) {
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
    for (int k = 0; k < (int)tokens.size(); k++) {
        if (k) cout << " ";
        cout << tokens[k];
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n) || n == 0) {
        serialize(nullptr);
        return 0;
    }
    vector<int> preorder(n), inorder(n);
    for (int i = 0; i < n; i++) cin >> preorder[i];
    for (int i = 0; i < n; i++) cin >> inorder[i];
    serialize(build_tree(preorder, inorder));
    return 0;
}
```
