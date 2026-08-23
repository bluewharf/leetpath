## 思路

- 不用除法：`answer[i]` 等于「左边所有数的积 × 右边所有数的积」。
- 从左扫一遍，把每个位置的前缀积先写进 `answer[i]`（此时还不含自己）。
- 再从右扫一遍，用一个后缀积变量乘回去，两次扫描后就是除自身外的乘积。
- 数组里的 0 不需要特判：0 左边/右边的积会自然落到正确位置。

## 复杂度

- 时间：O(n)
- 空间：O(1) 额外（不计答案数组）

## 模板代码

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
        ans[i] = pref
        pref *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= suf
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
    vector<long long> nums(n), ans(n, 1);
    for (int i = 0; i < n; i++) cin >> nums[i];
    long long pref = 1;
    for (int i = 0; i < n; i++) {
        ans[i] = pref;
        pref *= nums[i];
    }
    long long suf = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= suf;
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
