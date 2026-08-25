## 思路

本题常见有两种写法。面试先讲推荐解，再补备选。

### 解法一：排序 + 相向双指针（推荐）
- 先排序，再枚举最小元 `i`，剩下两个数用左右指针找相反数，把三数之和压成有序的两数之和。
- 相同值挤在一起：跳过与前一个相同的 `i` / `l` / `r`，三元组作为多重集合就不会重复。
- 固定 `i` 后和偏小只动左指针、偏大只动右指针；找到一组后左右同时收缩并去重。
- 最小元已经为正时后面全是更大的正数，不可能再凑出 0，直接收工。
- 每个 `i` 线性扫一遍，排序之外总时间平方级。模板即此写法。

### 解法二：枚举两数 + 哈希找第三数
- 枚举 `i`、`j`，用哈希表查 `-(nums[i]+nums[j])` 是否在后面出现。
- 去重要同时管「下标不能复用」和「同一组数不同顺序」，比有序双指针更容易漏。
- 时间同样 O(n²)，但哈希表要 O(n) 额外空间，常数通常更大。
- 更适合「只需判断是否存在」或不会写双指针去重时的退路；本题要输出全部不重复三元组，面试仍应落到解法一。

## 复杂度

- 解法一：时间 O(n²)，空间 O(1)（不计输出；排序可视为原地）
- 解法二：时间 O(n²)，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    nums.sort()
    for i in range(n):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                print(nums[i], nums[l], nums[r])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1


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
    if (!(cin >> n)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) cin >> nums[i];
    sort(nums.begin(), nums.end());
    for (int i = 0; i < n; ++i) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        if (nums[i] > 0) break;
        int l = i + 1, r = n - 1;
        while (l < r) {
            long long s = 1LL * nums[i] + nums[l] + nums[r];
            if (s < 0) {
                ++l;
            } else if (s > 0) {
                --r;
            } else {
                cout << nums[i] << ' ' << nums[l] << ' ' << nums[r] << '\n';
                ++l;
                --r;
                while (l < r && nums[l] == nums[l - 1]) ++l;
                while (l < r && nums[r] == nums[r + 1]) --r;
            }
        }
    }
    return 0;
}
```
