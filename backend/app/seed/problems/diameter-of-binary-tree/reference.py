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


def diameter(root):
    ans = 0

    def height(node):
        nonlocal ans
        if node is None:
            return 0
        left_height = height(node.left)
        right_height = height(node.right)
        ans = max(ans, left_height + right_height)
        return 1 + max(left_height, right_height)

    height(root)
    return ans


def main():
    print(diameter(read_tree()))


if __name__ == "__main__":
    main()
