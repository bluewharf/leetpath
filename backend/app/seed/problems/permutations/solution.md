## 思路

### 解法一（推荐）：排序后回溯

- 回溯生成全排列：路径表示当前排列，`used` 标记已经选过的下标。
- 先把 `nums` 排序，每一层按数组下标从左到右枚举未用元素，生成顺序就是字典序，输出时不必再排序。
- 递归到底（路径长度等于 `n`）就打印一行；回溯时撤销选择，继续试下一个。
- 题目保证元素互不相同，不需要「相同值跳过」的去重剪枝。

### 解法二：原地交换

- `dfs(i)`：把 `i .. n-1` 中每个位置与 `i` 交换，再递归 `i+1`，回溯时换回来。
- 省掉 `used` 数组，但不变量是「下标排列」而不是「按值从左到右选」，生成顺序一般不是字典序。
- 本题要按字典序输出，必须先收集再排序，所以不如解法一直接。

### 解法三：next_permutation 迭代

- 先排序，再反复求下一个排列直到绕回（或失败）。
- 无递归，输出天然字典序，依赖「下一个排列」那道题的三步。
- 与回溯相比：少了显式搜索树，但每一步都要找拐点，常数相当。

## 复杂度

- 解法一：时间 O(n · n!)，空间 O(n)（递归栈与 used，不计输出）
- 解法二：时间 O(n · n! + n! log n!)（若需再按字典序排序），空间 O(n)
- 解法三：时间 O(n · n!)，空间 O(1) 额外（不计输出）

## 模板代码

以下为实现 **解法一（推荐）** 的完整 ACM 程序，可通过本题全部用例。

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1 : 1 + n]))
    nums.sort()  # 先排序，按值从左到右选，生成顺序即字典序
    used = [False] * n
    path: list[int] = []

    def dfs() -> None:
        if len(path) == n:  # 排满 n 个，输出一行
            print(*path)
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False  # 回溯：下标 i 腾出来给同层后续选择
            # 题目保证元素互异，无需「相同值跳过」的去重剪枝

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
    if ((int)path.size() == n) {  // 排满 n 个，输出一行
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
        used[i] = 0;  // 回溯腾出下标；元素互异，无需相同值剪枝
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    nums.resize(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    sort(nums.begin(), nums.end());  // 先排序，生成顺序即字典序
    used.assign(n, 0);
    dfs();
    return 0;
}
```
