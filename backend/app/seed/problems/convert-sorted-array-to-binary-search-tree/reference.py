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
