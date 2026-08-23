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
