## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：中点递归建平衡 BST（推荐）
- 有序数组取中点当根、左右递归，中序天然有序，高度也平衡。
- 力扣原题允许任意平衡 BST，本题要答案唯一：闭区间 `[l, r]` 取 `mid = (l + r + 1) // 2`，偶数个元素时偏右。
- 这条规则等价于对每个子数组取下标 `len // 2`；空区间返回空节点。
- 平衡保证递归深度 O(log n)。建完按层序输出，末尾连续 `null` 省略，空树输出 `0`。
- 模板即此写法；中点公式写错会整棵树对不上。

### 解法二：栈模拟同一套中点规则
- 把区间 `[l, r]` 压栈，弹出后用同样的偏右中点建节点，再把左右子区间入栈。
- 生成的树与解法一完全一致，只是把递归改成显式栈，避免深度限制。
- 时间仍 O(n)，额外空间 O(h)（平衡时 O(log n)），再加上整棵树本身。
- 要求「不用递归」时用；默认递归更短、更不容易把中点公式写乱。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)（树节点；递归栈 O(log n)）
- 解法二：时间 O(n)，空间 O(n)（树节点；显式栈 O(log n)）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：有序数组取偏右中点当根，递归建平衡 BST。
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(nums, left, right):
    if left > right:
        return None  # 空区间
    mid = (left + right + 1) // 2  # 偶数个元素偏右，保证答案唯一
    node = TreeNode(nums[mid])
    node.left = build(nums, left, mid - 1)
    node.right = build(nums, mid + 1, right)
    return node


def write_tree(root):
    # ACM 输出：层序序列化，丢掉末尾连续 null；空树输出 0。
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
// 解法一：有序数组取偏右中点当根，递归建平衡 BST。
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* build(const vector<int>& nums, int left, int right) {
    if (left > right) return nullptr;  // 空区间
    int mid = (left + right + 1) / 2;  // 偶数个元素偏右，保证答案唯一
    TreeNode* node = new TreeNode(nums[mid]);
    node->left = build(nums, left, mid - 1);
    node->right = build(nums, mid + 1, right);
    return node;
}

void write_tree(TreeNode* root) {
    // ACM 输出：层序序列化，丢掉末尾连续 null；空树输出 0。
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
