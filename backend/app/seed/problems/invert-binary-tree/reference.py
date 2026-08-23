import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def read_tree():
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
        else:
            tokens.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    print(len(tokens))
    print(" ".join(tokens))


def invert(root):
    if root is None:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root


def main():
    write_tree(invert(read_tree()))


if __name__ == "__main__":
    main()
