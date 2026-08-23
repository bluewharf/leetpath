import heapq
import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def consume_list(lines: list[str], i: int) -> tuple[ListNode | None, int]:
    n = int(lines[i].strip())
    i += 1
    if n == 0:
        return None, i
    vals = list(map(int, lines[i].split()))
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next, i + 1


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


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap: list[tuple[int, int, ListNode]] = []
    for idx, node in enumerate(lists):
        if node is not None:
            heapq.heappush(heap, (node.val, idx, node))
    dummy = ListNode()
    cur = dummy
    while heap:
        _, idx, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    return dummy.next


def main() -> None:
    lines = sys.stdin.read().splitlines()
    k = int(lines[0].strip())
    lists: list[ListNode | None] = []
    i = 1
    for _ in range(k):
        head, i = consume_list(lines, i)
        lists.append(head)
    write_list(merge_k_lists(lists))


if __name__ == "__main__":
    main()
