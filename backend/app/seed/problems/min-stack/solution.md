## 思路

### 解法一：辅助栈同步最小值（推荐）

- 普通栈只能 O(1) 做 top/pop，最小值若每次扫描就是 O(n)；用辅助栈同步记录「当前栈内最小值」。
- `push(val)`：元素进数据栈；仅当辅助栈空或 `val <=` 辅助栈顶时，再把 `val` 压进辅助栈（等于也压，才能正确处理重复最小值）。
- `pop`：数据栈弹出的值若等于辅助栈顶，辅助栈同步弹出，当前最小值回退到上一层。
- `getMin` 就是辅助栈顶，与 `top` 一样都是 O(1)。
- 无返回值的操作按题面输出 `null`，有返回值的各打一行。

### 解法二：每个元素存当时最小值

- 栈里放 `(val, 当前min)`，`push` 时取 `min(val, 栈顶min)`（空栈则就是 `val`）。
- `getMin` 读栈顶第二项，不必单独辅助栈。
- 空间始终 O(n)；解法一在最小值不刷新时辅助栈更短，语义也更贴近「只在需要时同步」。

### 解法三：差值编码

- 只存 `val - 当前min`，再用一个变量记 min；弹出负差值时还原旧 min。
- 额外空间更省，但要处理溢出，且「负差值表示新最小值」容易写错。
- 面试默写风险高，提交用解法一。

## 复杂度

- 解法一：每个操作时间 O(1)，空间 O(q)
- 解法二：每个操作时间 O(1)，空间 O(q)
- 解法三：每个操作时间 O(1)，空间 O(q)（只多一个 min 变量，栈内仍是 O(q) 差值）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：辅助栈同步当前最小值；等于也压，才能正确 pop 重复最小值。
import sys


class MinStack:
    def __init__(self):
        self.st = []
        self.mins = []  # 同步「当前栈内最小值」；等于也压，才能正确 pop 重复最小值

    def push(self, val):
        self.st.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)

    def pop(self):
        val = self.st.pop()
        if val == self.mins[-1]:
            self.mins.pop()  # 弹出的恰是当前最小值，min 回退到上一层

    def top(self):
        return self.st[-1]

    def getMin(self):
        return self.mins[-1]


def main():
    # 操作序列：构造/push/pop 输出 null，top/getMin 输出值。
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
// 解法一：辅助栈同步当前最小值；等于也压，才能正确 pop 重复最小值。
#include <bits/stdc++.h>
using namespace std;

class MinStack {
    vector<int> st, mins;
public:
    void push(int val) {
        st.push_back(val);
        if (mins.empty() || val <= mins.back()) mins.push_back(val);  // 等于也压
    }
    void pop() {
        int val = st.back();
        st.pop_back();
        if (val == mins.back()) mins.pop_back();  // 同步回退当前最小值
    }
    int top() { return st.back(); }
    int getMin() { return mins.back(); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;  // 操作序列：无返回输出 null
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
