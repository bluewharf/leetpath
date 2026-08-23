import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def read_list() -> ListNode | None:
    data = sys.stdin.read().split()
    n = int(data[0])
    if n == 0:
        return None
    dummy = ListNode()
    cur = dummy
    for v in data[1 : 1 + n]:
        cur.next = ListNode(int(v))
        cur = cur.next
    return dummy.next


def is_palindrome(head: ListNode | None) -> bool:
    if head is None or head.next is None:
        return True
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    pre, cur = None, slow.next
    while cur:
        nxt = cur.next
        cur.next = pre
        pre, cur = cur, nxt
    while pre:
        if pre.val != head.val:
            return False
        pre = pre.next
        head = head.next
    return True


def main() -> None:
    print("true" if is_palindrome(read_list()) else "false")


if __name__ == "__main__":
    main()
