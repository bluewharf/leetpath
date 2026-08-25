## 思路

### 解法一（推荐）：全部异或

- 出现两次的数用异或会互相抵消：`x ^ x = 0`，且 `x ^ 0 = x`。
- 异或满足交换律和结合律，顺序无关，全部异或完只剩下那个出现一次的数。
- 不需要哈希表或排序，线性扫一遍、常数额外空间即可。
- 负数在补码表示下异或同样成立，直接按整数位运算即可。

### 解法二：哈希计数

- 用哈希表统计每个数出现次数，最后找出现恰好一次的那个。
- 不变量简单，也适用于「其余出现 k 次」的变体，但额外空间 O(n)。
- 与解法一差在：没有利用「出现两次」这一位运算结构。

### 解法三：排序后找不成对

- 排序后相邻两个一组比较，落单的就是答案；若都成对则答案是最后一个。
- 正确但打破 O(n)/O(1) 的最优约束，面试里当「想不到异或」的保底。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n)，空间 O(n)
- 解法三：时间 O(n log n)，空间 O(1)（就地排序）或 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    x = 0
    for v in nums:
        x ^= v
    print(x)


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
    int x = 0;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        x ^= v;
    }
    cout << x << '\n';
    return 0;
}
```
