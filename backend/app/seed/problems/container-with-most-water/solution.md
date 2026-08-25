## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：对撞双指针（推荐）
- 左右从两端往中间收，面积由「短板高度 × 宽度」决定。
- 宽度只会变小，想让面积变大，只能指望短板升高，所以每次把更矮的那一侧内移。
- 移动较高一侧没有意义：新高度仍被另一侧短板卡住，宽还变窄，面积不可能更好。
- 两边一样高时任意内移一侧即可（模板与参考解一致：内移右指针）。
- 每个位置最多被访问一次，扫完即得全局最大。

### 解法二：枚举两端
- 双重循环枚举左端 `i`、右端 `j`，面积 `min(h[i], h[j]) * (j-i)`，取最大。
- 正确但时间 O(n²)。本题 `n` 到 `10^5`，必超时，只适合数据极小或用来对照正确性。
- 由此能看出解法一把「不可能更优」的一侧直接丢掉。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n²)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：对撞双指针。宽只会变小，每次内移更矮的一侧指望短板升高。
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
            l += 1  # 短板在左，内移左指针才可能升高
        else:
            best = max(best, hr * (r - l))
            r -= 1  # 等高时任意内移一侧；与参考解一致：内移右指针
    print(best)


if __name__ == "__main__":
    main()
```


### C++

```cpp
// 解法一：对撞双指针。宽只会变小，每次内移更矮的一侧指望短板升高。
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
            l++;  // 短板在左，内移左指针才可能升高
        } else {
            best = max(best, hr * (r - l));
            r--;  // 等高时任意内移一侧；与参考解一致：内移右指针
        }
    }
    cout << best << "\n";
    return 0;
}
```

