## 思路

- 第 `i` 行（从 0 计）长度为 `i + 1`，两端恒为 1。
- 中间项 `row[j] = 上一行[j-1] + 上一行[j]`，对应组合数递推 `C(i,j) = C(i-1,j-1) + C(i-1,j)`。
- 逐行生成，只依赖上一行；边生成边按空格分隔输出。

## 复杂度

- 时间：O(numRows²)
- 空间：O(numRows)（只保留上一行）

## 模板代码

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
