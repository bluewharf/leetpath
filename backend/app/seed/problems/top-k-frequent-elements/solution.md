## 思路

- 先哈希计数，把「求前 k 高频」变成对去重后的键排序，不必真的维护堆也能一次出确定序。
- 本题输出有确定性约束：频次降序，同频按元素值升序；排序键用 `(-freq, value)` 即可。
- 只对不同元素排序，长度是去重后的 u（u ≤ n），比整段数组排序更干净。
- k 保证不超过不同元素个数，直接切前 k 个，不用再处理不足 k 的情况。
- 堆做法同样可以，但要同时满足「同频按值」需要自定义比较，排序更直白。

## 复杂度

- 时间：O(n + u log u)，u 为不同元素个数
- 空间：O(u)

## 模板代码

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
