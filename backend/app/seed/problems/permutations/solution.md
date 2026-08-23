## 思路

- 回溯生成全排列：路径表示当前排列，`used` 标记已经选过的下标。
- 先把 `nums` 排序，每一层按数组下标从左到右枚举未用元素，生成顺序就是字典序，输出时不必再排序。
- 递归到底（路径长度等于 `n`）就打印一行；回溯时撤销选择，继续试下一个。
- 题目保证元素互不相同，不需要「相同值跳过」的去重剪枝。

## 复杂度

- 时间：O(n · n!)
- 空间：O(n)（递归栈与 used，不计输出）

## 模板代码

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    nums.sort()
    used = [False] * n
    path: list[int] = []

    def dfs() -> None:
        if len(path) == n:
            print(*path)
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False

    dfs()


if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> nums, path;
vector<char> used;

void dfs() {
    if ((int)path.size() == n) {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << path[i];
        }
        cout << '\n';
        return;
    }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        used[i] = 1;
        path.push_back(nums[i]);
        dfs();
        path.pop_back();
        used[i] = 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    nums.resize(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    sort(nums.begin(), nums.end());
    used.assign(n, 0);
    dfs();
    return 0;
}
```
