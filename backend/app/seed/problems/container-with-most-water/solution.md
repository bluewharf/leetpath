## 思路

- 对撞双指针：左右从两端往中间收，面积由「短板高度 × 宽度」决定。
- 宽度只会变小，想让面积变大，只能指望短板升高，所以每次把更矮的那一侧内移。
- 移动较高一侧没有意义：新高度仍被另一侧短板卡住，宽还变窄，面积不可能更好。
- 两边一样高时任意内移一侧即可（本题与参考解一致：内移右指针）。
- 每个位置最多被访问一次，扫完即得全局最大。

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
    h = list(map(int, data[1 : 1 + n]))
    l, r = 0, n - 1
    best = 0
    while l < r:
        hl, hr = h[l], h[r]
        if hl < hr:
            best = max(best, hl * (r - l))
            l += 1
        else:
            best = max(best, hr * (r - l))
            r -= 1
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
    vector<int> h(n);
    for (int i = 0; i < n; i++) cin >> h[i];
    int l = 0, r = n - 1, best = 0;
    while (l < r) {
        int hl = h[l], hr = h[r];
        if (hl < hr) {
            best = max(best, hl * (r - l));
            l++;
        } else {
            best = max(best, hr * (r - l));
            r--;
        }
    }
    cout << best << "\n";
    return 0;
}
```
