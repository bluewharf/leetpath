import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    if n == 0:
        print("false")
        return
    vals = list(map(int, data[1 : 1 + n]))
    pos = int(data[1 + n])
    nodes = [ListNode(v) for v in vals]
    for i in range(n - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < n:
        nodes[-1].next = nodes[pos]
    slow = fast = nodes[0]
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            print("true")
            return
    print("false")


if __name__ == "__main__":
    main()
