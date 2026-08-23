import sys
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)


def main():
    q = int(sys.stdin.readline())
    cache = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "LRUCache":
            cache = LRUCache(int(parts[1]))
            print("null")
        elif op == "put":
            cache.put(int(parts[1]), int(parts[2]))
            print("null")
        elif op == "get":
            print(cache.get(int(parts[1])))


if __name__ == "__main__":
    main()
