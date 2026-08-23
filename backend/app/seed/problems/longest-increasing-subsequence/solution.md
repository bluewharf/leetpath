## 思路

- 维护 `tails[k]`：所有长度为 `k+1` 的严格递增子序列中，最小的可能结尾。
- `tails` 本身严格递增，对新来的 `x` 用二分找第一个 `>= x` 的位置替换（严格递增所以是 `bisect_left` / `lower_bound`）。
- 替换不增加长度，只让「同样长」的结尾更小，给后面更大的数留下增长空间。
- 若 `x` 比所有结尾都大则追加，LIS 长度加一。
- `tails` 的长度等于 LIS 长度；它本身不一定是某条真实子序列。

## 复杂度

- 时间：O(n log n)
- 空间：O(n)

## 模板代码

### Python3

```python
import bisect
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    tails: list[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    print(len(tails))


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
    vector<int> tails;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    cout << (int)tails.size() << "\n";
    return 0;
}
```
