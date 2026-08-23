## 思路

- 排序后枚举最小元，剩下两个数用相向双指针找相反数，把「三数之和」压成有序的两数之和。
- 有序数组上相同值挤在一起：跳过与前一个相同的 `i` / `l` / `r`，三元组作为多重集合就不会重复。
- 固定 `i` 后和偏小只动左指针、偏大只动右指针，每个 `i` 线性扫一遍，总时间平方级。
- 最小元已经为正时，后面全是更大的正数，不可能再凑出 0，直接收工。
- 找到一组后左右同时收缩并去重，避免同一对补数被反复输出。

## 复杂度

- 时间：O(n²)（排序 O(n log n)，每个 i 配一次双指针）
- 空间：O(1) 额外空间（不计输出；排序可视为原地）

## 模板代码

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
