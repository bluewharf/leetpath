import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def read_list():
    n = int(sys.stdin.readline())
    if n == 0:
        return None
    vals = list(map(int, sys.stdin.readline().split()))
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def write_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(1)
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))

def add(l1, l2):
    dummy = ListNode()
    cur = dummy
    carry = 0
    while l1 or l2 or carry:
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        carry = s // 10
        cur.next = ListNode(s % 10)
        cur = cur.next
    return dummy.next

def main():
    write_list(add(read_list(), read_list()))

if __name__ == "__main__":
    main()
