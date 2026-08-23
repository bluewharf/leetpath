import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def read_list():
    n = int(sys.stdin.readline())
    if n == 0:
        k = int(sys.stdin.readline())
        return None, k
    vals = list(map(int, sys.stdin.readline().split()))
    k = int(sys.stdin.readline())
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next, k

def write_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    print(len(vals))
    if vals:
        print(" ".join(vals))

def remove_nth(head, k):
    dummy = ListNode(0, head)
    fast = dummy
    for _ in range(k):
        fast = fast.next
    slow = dummy
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next

def main():
    head, k = read_list()
    write_list(remove_nth(head, k))

if __name__ == "__main__":
    main()
