## 思路

- 单调栈：栈里存下标，对应温度严格递减，专门等「下一个更高温度」。
- 今天比栈顶热，栈顶那天的答案就是「今天下标 − 栈顶下标」，弹出后继续比。
- 弹完把今天入栈；扫完仍留在栈里的天后面再也没有更高温度，答案保持 0。
- 每个下标最多进栈、出栈一次。
- 从左到右扫一遍即可得到全部等待天数。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    temps = data[1 : 1 + n]
    ans = [0] * n
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> temps(n);
    for (int i = 0; i < n; i++) cin >> temps[i];
    vector<int> ans(n, 0);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && temps[stack.back()] < temps[i]) {
            int j = stack.back();
            stack.pop_back();
            ans[j] = i - j;
        }
        stack.push_back(i);
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
```
