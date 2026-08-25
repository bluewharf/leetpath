## 思路

### 解法一（推荐）：哈希计数 + 排序

- 先哈希计数，把「求前 k 高频」变成对去重后的键排序，不必真的维护堆也能一次出确定序。
- 本题输出有确定性约束：频次降序，同频按元素值升序；排序键用 `(-freq, value)` 即可。
- 只对不同元素排序，长度是去重后的 u（u ≤ n），比整段数组排序更干净。
- k 保证不超过不同元素个数，直接切前 k 个，不用再处理不足 k 的情况。
- 堆 / 桶同样能取前 k，但要同时满足「同频按值」还得再排一次，排序最直白。

### 解法二：堆

- 计数后用大小为 k 的小根堆，或对全部键建堆后弹出 k 次。
- 比较器必须是「频次升序、同频按值降序」（小根堆里留下的是最终答案），否则同频顺序会乱。
- 与解法一差在：维护堆是为了 k ≪ u 时少排一些元素；本题还要全序输出，收益不明显。

### 解法三：频次桶

- 开 `n+1` 个桶，把值丢进 `桶[出现次数]`，再从高频桶往回扫，凑满 k 个。
- 同频桶内还要按值排序，才能满足本题的确定性输出。
- 时间期望 O(n)，但要额外 O(n) 桶；k 和值域都不大时很合适，实现比排序啰嗦。

## 复杂度

- 解法一：时间 O(n + u log u)，空间 O(u)，u 为不同元素个数
- 解法二：时间 O(n + u log k) 或 O(n + u log u)，空间 O(u)
- 解法三：时间 O(n + u log u)（同频排序），空间 O(n + u)

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys
from collections import Counter


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    k = int(data[n + 1])
    cnt = Counter(nums)
    ranked = sorted(cnt.keys(), key=lambda x: (-cnt[x], x))
    print(" ".join(str(x) for x in ranked[:k]))


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
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int k;
    cin >> k;
    unordered_map<int, int> cnt;
    cnt.reserve(n * 2);
    for (int x : nums) cnt[x]++;
    vector<int> keys;
    keys.reserve(cnt.size());
    for (auto& p : cnt) keys.push_back(p.first);
    sort(keys.begin(), keys.end(), [&](int a, int b) {
        if (cnt[a] != cnt[b]) return cnt[a] > cnt[b];
        return a < b;
    });
    for (int i = 0; i < k; i++) {
        if (i) cout << " ";
        cout << keys[i];
    }
    cout << "\n";
    return 0;
}
```
