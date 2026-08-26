import heapq
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    idx = 3
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for _ in range(m):
        a, b = data[idx], data[idx + 1]
        graph[b].append(a)
        indeg[a] += 1
        idx += 2
    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    if len(order) < n:
        return
    print(" ".join(map(str, order)))


if __name__ == "__main__":
    main()
