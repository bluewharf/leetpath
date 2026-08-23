## 思路

- 有序数组取中点当根、左右递归，中序天然有序，高度也平衡。
- 力扣原题允许任意平衡 BST，本题要答案唯一：闭区间 `[l, r]` 取 `mid = (l + r + 1) // 2`，偶数个元素时偏右。
- 这条规则等价于对每个子数组取下标 `len // 2`。
- 空区间返回空节点；平衡保证递归深度是 O(log n)。
- 建完按层序输出，末尾连续 `null` 省略，空树输出 `0`。

## 复杂度

- 时间：O(n)
- 空间：O(n)

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


def build(nums, left, right):
    if left > right:
        return None
    mid = (left + right + 1) // 2
    node = TreeNode(nums[mid])
    node.left = build(nums, left, mid - 1)
    node.right = build(nums, mid + 1, right)
    return node


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


def main():
    n = int(sys.stdin.readline().strip())
    if n == 0:
        nums = []
    else:
        nums = list(map(int, sys.stdin.readline().split()))
    root = build(nums, 0, n - 1)
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
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* build(const vector<int>& nums, int left, int right) {
    if (left > right) return nullptr;
    int mid = (left + right + 1) / 2;
    TreeNode* node = new TreeNode(nums[mid]);
    node->left = build(nums, left, mid - 1);
    node->right = build(nums, mid + 1, right);
    return node;
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
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    write_tree(build(nums, 0, n - 1));
    return 0;
}
```
