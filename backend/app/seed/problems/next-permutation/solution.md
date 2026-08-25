## 思路

### 解法一（推荐）：找拐点 + 交换后继 + 反转后缀

- 下一个排列是字典序刚好比当前大的那个；若不存在，则翻成最小序。
- 从右往左找第一个升序拐点 `i`（`a[i] < a[i+1]`）：它是必须变大的最右位置，左边不动才能让增幅最小。
- `i` 右侧一定非严格递减；再从右找第一个 `> a[i]` 的 `a[j]` 交换，新的 `a[i]` 是「刚好比原来大」的后继。
- 交换后右侧仍递减，反转这段得到最小后缀，整体即下一个排列。
- 找不到拐点说明整段递减，整段反转变升序。全程原地、只借常数额外空间。

### 解法二：后缀二分找后继

- 框架与解法一相同：先线性找到拐点 `i`。
- 右侧递减，可在这段上二分（或对升序拷贝 `lower_bound`）定位最右一个 `> a[i]` 的位置。
- 查找从线性变成对数，但找拐点仍是 O(n)，本题长度通常不大，常数未必更好。
- 交换、反转后缀两步不变，只是「找后继」的实现不同。

### 解法三：调用库的 next_permutation

- C++ `std::next_permutation` 的语义就是解法一这三步，失败时把序列翻成升序。
- 封装省事，但面试必须能讲清拐点、后继、反转，不能只会调库。
- 有重复元素时规则不变：后继取「严格更大」的最右者，自然跳过相同排列。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(1)（找拐点仍是线性）
- 解法三：时间 O(n)，空间 O(1)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def next_permutation(a: list[int]) -> None:
    n = len(a)
    i = n - 2
    # 从右找第一个升序拐点：它是必须变大的最右位置，左边保持不动增幅才最小
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        # 右侧非严格递减，从右取第一个 > a[i] 的后继，交换后新前缀刚好变大
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    # 边界：找不到拐点则整段递减，反转即最小排列；有拐点时右侧仍递减，反转变最小后缀
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
    if (n <= 1) return;  // 边界：空/单元素已是唯一排列
    int i = n - 2;
    // 从右找第一个升序拐点：必须变大的最右位置，左边不动才能让增幅最小
    while (i >= 0 && a[i] >= a[i + 1]) --i;
    if (i >= 0) {
        int j = n - 1;
        // 右侧非严格递减，从右取第一个 > a[i] 的后继
        while (a[j] <= a[i]) --j;
        swap(a[i], a[j]);
    }
    // 找不到拐点则整段递减，反转即最小排列；有拐点时反转后缀得到最小后缀
    reverse(a.begin() + i + 1, a.end());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;  // 读入：第一行 n，随后 n 个数
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
