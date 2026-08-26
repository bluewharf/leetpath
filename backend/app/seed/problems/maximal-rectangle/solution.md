## 思路

逐行把「当前行向上连续 1 的高度」当成直方图，对每一行求柱状图最大矩形，取全局最大。

### 解法一（推荐）：高度累加 + 单调栈

- `height[j]`：第 `j` 列从当前行向上连续 1 的个数；遇 0 清零。
- 对 `height` 用单调递增栈：弹出时宽 = `i - stack[-1] - 1`，末尾补 0 清空。
- 和 LC84 同一核心，先会直方图再套到二维。

### 解法二：对每个点向右下暴力扩

- n 很小才能过。面试用来说明为什么要栈。

## 复杂度

- 解法一：时间 O(mn)，空间 O(n)
- 解法二：时间 O(m²n²)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def largest_rectangle(heights: list[int]) -> int:
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


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    height = [0] * n
    ans = 0
    for i in range(m):
        for j in range(n):
            height[j] = height[j] + 1 if mat[i][j] == 1 else 0
        area = largest_rectangle(height)
        if area > ans:
            ans = area
    print(ans)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int largest_rectangle(vector<int> heights) {
    heights.push_back(0);
    vector<int> st;
    st.push_back(-1);
    int ans = 0;
    for (int i = 0; i < (int)heights.size(); ++i) {
        while (st.back() != -1 && heights[st.back()] > heights[i]) {
            int height = heights[st.back()];
            st.pop_back();
            int width = i - st.back() - 1;
            ans = max(ans, height * width);
        }
        st.push_back(i);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int>> mat(m, vector<int>(n));
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j) cin >> mat[i][j];
    vector<int> height(n, 0);
    int ans = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) height[j] = mat[i][j] == 1 ? height[j] + 1 : 0;
        ans = max(ans, largest_rectangle(height));
    }
    cout << ans << '\n';
    return 0;
}
```
