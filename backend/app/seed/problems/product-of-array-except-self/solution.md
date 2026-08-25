## 思路

### 解法一（推荐）：前缀积 × 后缀积，两次扫描

- 不用除法：`answer[i]` 等于「左边所有数的积 × 右边所有数的积」。
- 从左扫一遍，把每个位置的前缀积先写进 `answer[i]`（此时还不含自己）。
- 再从右扫一遍，用一个后缀积变量乘回去，两次扫描后就是除自身外的乘积。
- 数组里的 0 不需要特判：0 左边/右边的积会自然落到正确位置。

### 解法二：显式前缀/后缀数组

- 开 `pref[i]`、`suf[i]`，令 `answer[i] = pref[i] * suf[i]`。
- 与两次扫描同一思路，空间多 O(n)，但「左右积」一眼能看出来。
- 面试可先写这个，再压缩成解法一。

### 解法三：除法 + 统计 0

- 没有 0：全体积除以 `nums[i]`；恰好一个 0：只有该位置为其余积，别处为 0；两个以上全 0。
- 题目通常禁止除法，还要小心整数除与溢出。
- 和前两种比，少了「左右扫描」的构造，但对 0 的分类讨论容易漏。

## 复杂度

- 解法一：时间 O(n)，空间 O(1) 额外（不计答案数组）
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n)，空间 O(1) 额外

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : n + 1]
    ans = [1] * n
    pref = 1
    for i in range(n):
        ans[i] = pref  # 先写入不含自己的左侧积
        pref *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= suf  # 再乘不含自己的右侧积；0 会自然落到正确位置
        suf *= nums[i]
    print(" ".join(map(str, ans)))


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
    vector<long long> nums(n), ans(n, 1);  // 乘积可能超出 32 位
    for (int i = 0; i < n; i++) cin >> nums[i];
    long long pref = 1;
    for (int i = 0; i < n; i++) {
        ans[i] = pref;  // 先写入不含自己的左侧积
        pref *= nums[i];
    }
    long long suf = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= suf;  // 再乘不含自己的右侧积；0 会自然落到正确位置
        suf *= nums[i];
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```
