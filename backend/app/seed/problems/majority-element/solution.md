## 思路

- Boyer-Moore 投票：多数元素出现次数严格大于 `n/2`，把它记 +1、其它记 -1，全程净和一定为正。
- 维护当前候选人与计数；计数归零就换新候选人（前面的票被两两抵消完了）。
- 不同元素互相消耗后，最后留下的一定是多数——题目保证多数存在，无需第二轮验证。
- 一次遍历、常数额外空间，不必哈希计数。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    cand = 0
    cnt = 0
    for v in nums:
        if cnt == 0:
            cand = v
        cnt += 1 if v == cand else -1
    print(cand)


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
    int cand = 0, cnt = 0;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        if (cnt == 0) cand = v;
        cnt += (v == cand) ? 1 : -1;
    }
    cout << cand << "\n";
    return 0;
}
```
