## 思路

- 普通栈只能 O(1) 做 top/pop，最小值若每次扫描就是 O(n)；用辅助栈同步记录「当前栈内最小值」。
- `push(val)`：元素进数据栈；仅当辅助栈空或 `val <=` 辅助栈顶时，再把 `val` 压进辅助栈（等于也压，才能正确处理重复最小值）。
- `pop`：数据栈弹出的值若等于辅助栈顶，辅助栈同步弹出，当前最小值回退到上一层。
- `getMin` 就是辅助栈顶，与 `top` 一样都是 O(1)。
- 无返回值的操作按题面输出 `null`，有返回值的各打一行。

## 复杂度

- 时间：每个操作 O(1)
- 空间：O(q)

## 模板代码

### Python3

```python
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
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class MinStack {
    vector<int> st, mins;
public:
    void push(int val) {
        st.push_back(val);
        if (mins.empty() || val <= mins.back()) mins.push_back(val);
    }
    void pop() {
        int val = st.back();
        st.pop_back();
        if (val == mins.back()) mins.pop_back();
    }
    int top() { return st.back(); }
    int getMin() { return mins.back(); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    MinStack* stk = nullptr;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "MinStack") {
            stk = new MinStack();
            cout << "null\n";
        } else if (op == "push") {
            int val;
            cin >> val;
            stk->push(val);
            cout << "null\n";
        } else if (op == "pop") {
            stk->pop();
            cout << "null\n";
        } else if (op == "top") {
            cout << stk->top() << '\n';
        } else if (op == "getMin") {
            cout << stk->getMin() << '\n';
        }
    }
    return 0;
}
```
