import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
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
        print(" ".join(level))


if __name__ == "__main__":
    main()
