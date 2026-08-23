## 思路

- 以每根柱子为高的最大矩形，宽度由其左右第一个更矮柱子夹出来。
- 单调递增栈存下标：新来的柱子更矮，栈顶就是「右边界刚确定」的柱子，立刻结算面积。
- 弹出后新的栈顶是左侧第一个更矮的位置，宽 = `i - stack[-1] - 1`。
- 末尾补一根高度 0，把栈里剩下的柱子统一出栈，免得单独收尾。
- 栈底放 `-1` 当哨兵，最矮柱可以向左扩到下标 0。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


def largest_rectangle(heights):
    heights = heights + [0]
    stack = [-1]
    ans = 0
    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            area = height * width
            if area > ans:
                ans = area
        stack.append(i)
    return ans


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    h = list(map(int, data[1 : 1 + n]))
    print(largest_rectangle(h))


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
    vector<int> heights(n);
    for (int i = 0; i < n; i++) cin >> heights[i];
    heights.push_back(0);
    vector<int> stack;
    stack.push_back(-1);
    long long ans = 0;
    for (int i = 0; i < (int)heights.size(); i++) {
        while (stack.back() != -1 && heights[stack.back()] > heights[i]) {
            int height = heights[stack.back()];
            stack.pop_back();
            int width = i - stack.back() - 1;
            ans = max(ans, 1LL * height * width);
        }
        stack.push_back(i);
    }
    cout << ans << "\n";
    return 0;
}
```
