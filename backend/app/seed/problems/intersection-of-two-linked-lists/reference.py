import sys


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def read_vals(lines: list[str], i: int) -> tuple[list[int], int]:
    n = int(lines[i].strip())
    i += 1
    if n == 0:
        return [], i
    vals = list(map(int, lines[i].split()))
    return vals, i + 1


def build(vals: list[int]) -> tuple[ListNode | None, list[ListNode]]:
    dummy = ListNode()
    cur = dummy
    nodes: list[ListNode] = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    return dummy.next, nodes


def main() -> None:
    lines = sys.stdin.read().splitlines()
    i = 0
    vals_a, i = read_vals(lines, i)
    vals_b, i = read_vals(lines, i)
    skip_a, skip_b = map(int, lines[i].split())

    head_a, nodes_a = build(vals_a)
    if skip_a < 0:
        head_b, _ = build(vals_b)
    else:
        dummy = ListNode()
        cur = dummy
        for j in range(skip_b):
            cur.next = ListNode(vals_b[j])
            cur = cur.next
        cur.next = nodes_a[skip_a]
        head_b = dummy.next

    a, b = head_a, head_b
    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a
    print(-1 if a is None else a.val)


if __name__ == "__main__":
    main()
