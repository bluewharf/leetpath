import sys


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head):
    if head is None:
        return None
    mapping = {None: None}
    cur = head
    while cur:
        mapping[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        mapping[cur].next = mapping[cur.next]
        mapping[cur].random = mapping[cur.random]
        cur = cur.next
    return mapping[head]


def main():
    n = int(sys.stdin.readline())
    if n == 0:
        print(0)
        return
    vals = []
    rands = []
    for _ in range(n):
        parts = sys.stdin.readline().split()
        vals.append(int(parts[0]))
        rands.append(int(parts[1]))
    nodes = [Node(v) for v in vals]
    for i in range(n):
        if i + 1 < n:
            nodes[i].next = nodes[i + 1]
        if rands[i] != -1:
            nodes[i].random = nodes[rands[i]]
    copied = copy_random_list(nodes[0])
    arr = []
    cur = copied
    while cur:
        arr.append(cur)
        cur = cur.next
    idx = {node: i for i, node in enumerate(arr)}
    print(len(arr))
    for node in arr:
        ri = idx[node.random] if node.random is not None else -1
        print(node.val, ri)


if __name__ == "__main__":
    main()
