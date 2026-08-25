## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：单调递减栈（推荐）
- 栈里存下标，对应温度严格递减，专门等「下一个更高温度」。
- 今天比栈顶热，栈顶那天的答案就是「今天下标 − 栈顶下标」，弹出后继续比。
- 弹完把今天入栈；扫完仍留在栈里的天后面再也没有更高温度，答案保持 0。
- 每个下标最多进栈、出栈一次，从左到右一遍即可。模板即此写法。

### 解法二：从右往左按已算答案跳跃
- `ans` 先填 0。从右往左看：若后一天更热，答案就是 1；否则沿着 `i + ans[i]` 往右跳，直到找到更高或越界。
- 每个位置摊还 O(1) 次跳跃，时间也是 O(n)，不必显式栈。
- 实现细节比单调栈绕（要处理 `ans[j]==0` 表示后面没有更高），容易写出死循环或 O(n²)。
- `n` 到 `10^5`，暴力对每个 i 往右扫会超时，只能当错误对照。面试默认单调栈。

## 复杂度

- 解法一：时间 O(n)，空间 O(n)
- 解法二：时间 O(n)（摊还），空间 O(1)（不计答案数组）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：单调递减栈存下标，等下一个更高温度。
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    temps = data[1 : 1 + n]
    ans = [0] * n
    stack = []  # 栈内下标对应温度严格递减
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j  # 今天就是栈顶那天的下一个更高
        stack.append(i)
    # 扫完仍留在栈里的天后面再也没有更高，答案保持 0
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：单调递减栈存下标，等下一个更高温度。
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
    vector<int> stack;  // 栈内下标对应温度严格递减
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && temps[stack.back()] < temps[i]) {
            int j = stack.back();
            stack.pop_back();
            ans[j] = i - j;  // 今天就是栈顶那天的下一个更高
        }
        stack.push_back(i);
    }
    // 扫完仍留在栈里的天后面再也没有更高，答案保持 0
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
```

