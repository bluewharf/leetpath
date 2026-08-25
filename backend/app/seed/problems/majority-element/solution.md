## 思路

### 解法一：Boyer-Moore 投票（推荐）

- 多数元素出现次数严格大于 `n/2`，把它记 +1、其它记 -1，全程净和一定为正。
- 维护当前候选人与计数；计数归零就换新候选人（前面的票被两两抵消完了）。
- 不同元素互相消耗后，最后留下的一定是多数——题目保证多数存在，无需第二轮验证。
- 一次遍历、常数额外空间，不必哈希计数；若题目不保证存在，必须再扫一遍确认 `cand` 真的过半。

### 解法二：哈希计数

- 扫一遍统计频次，某值次数超过 `n/2` 即可返回。
- 实现最直观，和投票法差在「用 O(n) 空间换掉抵消过程」。
- 不依赖「严格过半」也能找出众数，但本题保证多数，空间是多余的。

### 解法三：排序取中位数

- 排序后下标 `n/2` 处一定是多数：它至少占满一半并盖住中点。
- 时间 O(n log n)，没有用上「可以线性做完」这一信息。
- 写起来极短，适合数据很小或已经要排序的变体。

## 复杂度

- 解法一：时间 O(n)，空间 O(1)
- 解法二：时间 O(n) 平均，空间 O(n)
- 解法三：时间 O(n log n)，空间 O(1) 或 O(n)（视排序而定）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    cand = 0
    cnt = 0
    for v in nums:
        if cnt == 0:
            cand = v
        cnt += 1 if v == cand else -1
    print(cand)


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
    int cand = 0, cnt = 0;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        if (cnt == 0) cand = v;
        cnt += (v == cand) ? 1 : -1;
    }
    cout << cand << "\n";
    return 0;
}
```
