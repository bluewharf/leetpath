## 思路

- 连续序列只看数值是否相邻，与原数组下标无关，先丢进哈希集合去重。
- 只从「段首」起步：当 `x-1` 不在集合里，`x` 才可能是一段的左端点。
- 从段首向右数 `x, x+1, ...` 直到断掉，长度就是终点减起点。
- 每个数最多作为段内元素被访问一次，避免对每个点都向两边扩展，整体线性。
- 空数组时集合为空，最长长度为 0。

## 复杂度

- 时间：O(n)
- 空间：O(n)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y in s:
                y += 1
            best = max(best, y - x)
    print(best)


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
    unordered_set<int> s;
    s.reserve(n * 2 + 1);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s.insert(x);
    }
    int best = 0;
    for (int x : s) {
        if (!s.count(x - 1)) {
            int y = x;
            while (s.count(y)) y++;
            best = max(best, y - x);
        }
    }
    cout << best << "\n";
    return 0;
}
```
