## 思路

- 路径必须向下、但不限定起终点，等于树上任意「祖先 → 当前节点」这一段的和，也就是树上的前缀和等于 `target`。
- 维护根到当前节点的前缀和 `curr`，这条路径上的答案贡献是历史上出现过多少次 `curr - target`。
- 用哈希表统计前缀出现次数：下钻前加一，回溯时减一（减到 0 就删掉），保证只统计当前这条祖先链。
- 空树答案为 0；节点值可负，同一前缀可能出现多次，必须计数而不是集合。
- 前缀和最大约 `1000 × 10^9`，C++ 用 64 位整数。

## 复杂度

- 时间：O(n)
- 空间：O(n)（哈希表 + 递归栈）

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
    if not tokens:
        return None
    root = TreeNode(int(tokens[0]))
    q = deque([root])
    i = 1
    n = len(tokens)
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


def path_sum(root, target):
    def dfs(node, curr, prefix):
        if not node:
            return 0
        curr += node.val
        ans = prefix.get(curr - target, 0)
        prefix[curr] = prefix.get(curr, 0) + 1
        ans += dfs(node.left, curr, prefix)
        ans += dfs(node.right, curr, prefix)
        prefix[curr] -= 1
        if prefix[curr] == 0:
            del prefix[curr]
        return ans

    return dfs(root, 0, {0: 1})


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    tokens = data[1 : 1 + n]
    target = int(data[1 + n])
    print(path_sum(build_tree(tokens), target))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    long long val;
    TreeNode *left, *right;
    TreeNode(long long v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* buildTree(const vector<string>& tokens) {
    if (tokens.empty()) return nullptr;
    TreeNode* root = new TreeNode(stoll(tokens[0]));
    queue<TreeNode*> q;
    q.push(root);
    int i = 1, n = (int)tokens.size();
    while (!q.empty() && i < n) {
        TreeNode* node = q.front();
        q.pop();
        if (i < n) {
            if (tokens[i] != "null") {
                node->left = new TreeNode(stoll(tokens[i]));
                q.push(node->left);
            }
            ++i;
        }
        if (i < n) {
            if (tokens[i] != "null") {
                node->right = new TreeNode(stoll(tokens[i]));
                q.push(node->right);
            }
            ++i;
        }
    }
    return root;
}

long long dfs(TreeNode* node, long long curr, long long target, unordered_map<long long, int>& prefix) {
    if (!node) return 0;
    curr += node->val;
    long long ans = 0;
    auto it = prefix.find(curr - target);
    if (it != prefix.end()) ans = it->second;
    ++prefix[curr];
    ans += dfs(node->left, curr, target, prefix);
    ans += dfs(node->right, curr, target, prefix);
    if (--prefix[curr] == 0) prefix.erase(curr);
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> tokens;
    tokens.reserve(n);
    for (int i = 0; i < n; ++i) {
        string t;
        cin >> t;
        tokens.push_back(t);
    }
    long long target;
    cin >> target;
    unordered_map<long long, int> prefix;
    prefix[0] = 1;
    cout << dfs(buildTree(tokens), 0, target, prefix) << '\n';
    return 0;
}
```
