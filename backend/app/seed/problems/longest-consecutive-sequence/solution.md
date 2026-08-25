## 思路

### 解法一：哈希集合从段首扩展（推荐）

- 连续序列只看数值是否相邻，与原下标无关，先丢进哈希集合去重。
- 只从「段首」起步：`x-1` 不在集合里，`x` 才是一段的左端点，再向右数 `x, x+1, ...` 直到断开。
- 不变量：每个数最多作为段内元素被访问一次；禁止对每个点都向两边扩，否则会退化成平方。
- 空数组时集合为空，最长长度为 0。
- 和排序比：用哈希平均 O(1) 查询换掉 `n log n` 比较，最坏依赖哈希实现。

### 解法二：排序后扫连续段

- 排序（可顺手去重）后线性扫：相邻差 1 则当前段长 +1，否则另起一段。
- 不变量：排完后同一连续段一定挤在一起；重复值必须跳过，否则 `1,1,2` 会被当成断开。
- 实现短、最坏时间确定，哈希被卡或禁止额外哈希时的保底写法。
- 和段首扩展差在「先全局排好再数」，不需要随机访问集合。

### 解法三：哈希表记录区间端点

- 插入 `x` 时查 `x-1`、`x+1` 已有段的长度，三段拼成新区间，只更新新段两端的长度即可。
- 每个数只插入一次也能线性，但重复值、端点漏更新都容易写错。
- 代码比段首扩展绕，面试默写不如解法一稳。

## 复杂度

- 解法一：时间 O(n) 平均，空间 O(n)
- 解法二：时间 O(n log n)，空间 O(n)（去重/排序；原地排序可压额外空间）
- 解法三：时间 O(n) 平均，空间 O(n)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
# 解法一：哈希集合只从段首扩展。x-1 不在集合里才向右数，避免平方扫描。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    s = set(nums)  # 只关心数值是否存在，下标无关；顺手去重
    best = 0
    for x in s:
        # 只从段首起步：x-1 已在集合里说明 x 不是左端点，否则会平方扫描。
        if x - 1 not in s:
            y = x
            while y in s:
                y += 1
            best = max(best, y - x)  # 半开区间 [x, y) 的长度
    print(best)  # 空数组时集合为空，best 保持 0


if __name__ == "__main__":
    main()
```

### C++

```cpp
// 解法一：哈希集合只从段首扩展。x-1 不在集合里才向右数，避免平方扫描。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    unordered_set<int> s;
    s.reserve(n * 2 + 1);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s.insert(x);
    }
    int best = 0;
    for (int x : s) {
        // 只从段首扩展：每个数作为段内元素至多被扫一次。
        if (!s.count(x - 1)) {
            int y = x;
            while (s.count(y)) y++;
            best = max(best, y - x);
        }
    }
    cout << best << "\n";
    return 0;
}
```
