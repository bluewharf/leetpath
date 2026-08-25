## 思路

### 解法一（推荐）：逐行递推

- 第 `i` 行（从 0 计）长度为 `i + 1`，两端恒为 1。
- 中间项 `row[j] = 上一行[j-1] + 上一行[j]`，对应组合数递推 `C(i,j) = C(i-1,j-1) + C(i-1,j)`。
- 逐行生成，只依赖上一行；边生成边按空格分隔输出。

### 解法二：同行组合数递推

- 同一行内 `C(i,j) = C(i,j-1) * (i-j+1) / j`，不必读上一行。
- 必须先乘后整除，保证始终整除；C++ 用 64 位防溢出。
- 适合只要第 `k` 行的变体；本题要全部行，整体仍是平方级。

### 解法三：原地从右往左滚动

- 在同一数组末尾添 1，然后从右往左 `a[j] += a[j-1]`，避免覆盖还没加过的旧值。
- 与解法一同一递推，少一次分配。
- 滚动方向反了会把新值重复累加，这是和「开新行」写法的主要差别。

## 复杂度

- 解法一：时间 O(numRows²)，空间 O(numRows)（只保留上一行）
- 解法二：时间 O(numRows²)，空间 O(numRows)
- 解法三：时间 O(numRows²)，空间 O(numRows)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    row = [1]
    print(1)
    for i in range(1, n):
        nxt = [1] * (i + 1)
        for j in range(1, i):
            nxt[j] = row[j - 1] + row[j]
        print(" ".join(str(x) for x in nxt))
        row = nxt


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
    vector<int> row = {1};
    cout << 1 << '\n';
    for (int i = 1; i < n; ++i) {
        vector<int> nxt(i + 1, 1);
        for (int j = 1; j < i; ++j) nxt[j] = row[j - 1] + row[j];
        for (int j = 0; j <= i; ++j) {
            if (j) cout << ' ';
            cout << nxt[j];
        }
        cout << '\n';
        row.swap(nxt);
    }
    return 0;
}
```
