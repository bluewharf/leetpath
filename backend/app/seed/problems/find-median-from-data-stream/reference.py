import heapq
import sys


class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap of the smaller half (store negated values)
        self.hi = []  # min-heap of the larger half

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


def main():
    q = int(sys.stdin.readline())
    mf = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "MedianFinder":
            mf = MedianFinder()
            print("null")
        elif op == "addNum":
            mf.addNum(int(parts[1]))
            print("null")
        elif op == "findMedian":
            print(f"{mf.findMedian():.1f}")


if __name__ == "__main__":
    main()
