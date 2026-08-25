## 思路

### 解法一：Kadane（推荐）

- 只关心「以 i 结尾」的最大子数组和，答案是这些值里的全局最大。
- `cur = max(nums[i], cur + nums[i])`：前面那段和若已经变负，再往后加只会拖后腿，直接从当前元素另起一段。
- 不变量：扫完 i 时，`cur` 一定是所有以 i 结尾的连续段里和最大的那个。
- 全是负数时会不断「另起一段」，最终落到最大的那个单元素，不会误返回 0。
- 一次遍历、常数空间，是本题默认提交写法。

### 解法二：前缀和

- 以位置 i 结尾的最大段 = `pre[i] - min(pre[j])`（`j < i`）；边走边维护目前前缀最小值即可。
- 和 Kadane 同是 O(n)/O(1)，只是把「丢掉负前缀」说成「减去最小前缀」。
- 若要输出左右端点，记下最小前缀出现的下标即可。

### 解法三：分治

- 答案在左半、右半，或跨越中点；跨越时从中点向两边扩展，取「左最大后缀 + 右最大前缀」。
- 时间 O(n log n)，对应线段树「区间最大子段和」的教学版本。
- 面试用来展示分治，提交不如 Kadane。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)
- 解法三：时间 O(n log n)，空间 O(log n)（递归栈）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：Kadane。前缀为负则丢掉，cur 是以当前位置结尾的最大段和。
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    # Kadane：cur 是「以当前元素结尾」的最大段和；前缀已为负则丢掉另起。
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur + x < x else cur + x
        if cur > best:
            best = cur
    print(best)  # 全负时不断另起，答案落到最大的那个单元素


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：Kadane。前缀为负则丢掉，cur 是以当前位置结尾的最大段和。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    long long best = nums[0], cur = nums[0];  // cur：以 i 结尾的最大连续和
    for (int i = 1; i < n; i++) {
        cur = max(nums[i], cur + nums[i]);  // 前缀为负则丢掉
        best = max(best, cur);
    }
    cout << best << '\n';
    return 0;
}
```
