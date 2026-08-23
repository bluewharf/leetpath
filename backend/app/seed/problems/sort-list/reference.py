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


def write_list(head: ListNode | None) -> None:
    vals: list[str] = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


def split(head: ListNode) -> ListNode:
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    return mid


def merge(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 if l1 else l2
    return dummy.next


def sort_list(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    mid = split(head)
    left = sort_list(head)
    right = sort_list(mid)
    return merge(left, right)


def main() -> None:
    write_list(sort_list(read_list()))


if __name__ == "__main__":
    main()
