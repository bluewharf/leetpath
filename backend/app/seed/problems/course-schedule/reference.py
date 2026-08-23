import sys
from collections import deque


def can_finish(n: int, prerequisites: list[tuple[int, int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    taken = 0
    while q:
        u = q.popleft()
        taken += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == n


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    idx = 3
    prereq = []
    for _ in range(m):
        prereq.append((data[idx], data[idx + 1]))
        idx += 2
    print("true" if can_finish(n, prereq) else "false")


if __name__ == "__main__":
    main()
