## 思路

- 柱 i 能接的水是 `min(左侧最高, 右侧最高) - height[i]`（非正则 0）；瓶颈永远是两侧较矮的那堵墙。
- 双指针从两端往中间走：谁更矮，谁这边的水位就已经被对侧保证（对侧至少有一根不低于它）。
- 维护 `left_max / right_max`：当前柱若刷新了这一侧的最高，它自己接不了水；否则水位就是该侧 max 减自身高度。
- 每次只结算更矮的一端并内收指针，每个下标恰好处理一次，O(1) 额外空间代替左右前缀数组。
- `l == r` 时这一格也会被结算一次，但它是当前两侧 max 的交汇处，加的水仍正确（通常为 0）。

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
    if n == 0:
        print(0)
        return
    l, r = 0, n - 1
    left_max, right_max = 0, 0
    ans = 0
    while l <= r:
        if h[l] <= h[r]:
            if h[l] >= left_max:
                left_max = h[l]
            else:
                ans += left_max - h[l]
            l += 1
        else:
            if h[r] >= right_max:
                right_max = h[r]
            else:
                ans += right_max - h[r]
            r -= 1
    print(ans)


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
    if (n == 0) {
        cout << 0 << "\n";
        return 0;
    }
    int l = 0, r = n - 1;
    int left_max = 0, right_max = 0;
    long long ans = 0;
    while (l <= r) {
        if (h[l] <= h[r]) {
            if (h[l] >= left_max) left_max = h[l];
            else ans += left_max - h[l];
            l++;
        } else {
            if (h[r] >= right_max) right_max = h[r];
            else ans += right_max - h[r];
            r--;
        }
    }
    cout << ans << "\n";
    return 0;
}
```
