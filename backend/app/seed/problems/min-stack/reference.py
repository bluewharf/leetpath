import sys


class MinStack:
    def __init__(self):
        self.st = []
        self.mins = []

    def push(self, val):
        self.st.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)

    def pop(self):
        val = self.st.pop()
        if val == self.mins[-1]:
            self.mins.pop()

    def top(self):
        return self.st[-1]

    def getMin(self):
        return self.mins[-1]


def main():
    q = int(sys.stdin.readline())
    stk = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "MinStack":
            stk = MinStack()
            print("null")
        elif op == "push":
            stk.push(int(parts[1]))
            print("null")
        elif op == "pop":
            stk.pop()
            print("null")
        elif op == "top":
            print(stk.top())
        elif op == "getMin":
            print(stk.getMin())


if __name__ == "__main__":
    main()
