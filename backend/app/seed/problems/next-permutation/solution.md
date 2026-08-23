## 思路

- 下一个排列就是字典序刚好比当前大的那个；若不存在，则翻成最小序。
- 从右往左找第一个升序拐点 `i`（`a[i] < a[i+1]`）：它是必须变大的最右位置，左边不动才能让增幅最小。
- `i` 右侧一定是非严格递减的。再从右找第一个 `> a[i]` 的 `a[j]` 与之交换，这样新的 `a[i]` 是「刚好比原来大」的后继。
- 交换后右侧仍递减，反转这段即得到最小后缀，整体就是下一个排列。
- 找不到拐点说明整个序列递减，整段反转变成升序。全程原地、只借常数额外空间。

## 复杂度

- 时间：O(n)
- 空间：O(1)

## 模板代码

### Python3

```python
import sys


def next_permutation(a: list[int]) -> None:
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1 :] = reversed(a[i + 1 :])


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    nums = data[1 : 1 + n]
    next_permutation(nums)
    print(*nums)


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

void nextPermutation(vector<int>& a) {
    int n = (int)a.size();
    if (n <= 1) return;
    int i = n - 2;
    while (i >= 0 && a[i] >= a[i + 1]) --i;
    if (i >= 0) {
        int j = n - 1;
        while (a[j] <= a[i]) --j;
        swap(a[i], a[j]);
    }
    reverse(a.begin() + i + 1, a.end());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    nextPermutation(a);
    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}
```
