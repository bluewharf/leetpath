# 力扣热题 100 清单（种子生成依据）

I/O 统一约定见 `docs/spec/seed-format.md`。"备注"列仅对需要特殊说明的题标注。

| # | slug | 标题 | 难度 | 标签 | 备注 |
|---|---|---|---|---|---|
| 1 | two-sum | 两数之和 | easy | 数组, 哈希表 | 输出两个下标（小在前），空格分隔 |
| 2 | group-anagrams | 字母异位词分组 | medium | 数组, 哈希表, 字符串 | 每组一行（组内字典序），组间按组内首元素字典序 |
| 3 | longest-consecutive-sequence | 最长连续序列 | medium | 并查集, 数组, 哈希表 | |
| 4 | move-zeroes | 移动零 | easy | 数组, 双指针 | 输出移动后的数组 |
| 5 | container-with-most-water | 盛最多水的容器 | medium | 贪心, 数组, 双指针 | |
| 6 | 3sum | 三数之和 | medium | 数组, 双指针, 排序 | 每行一个三元组（升序），组间字典序 |
| 7 | trapping-rain-water | 接雨水 | hard | 栈, 数组, 双指针, DP | |
| 8 | longest-substring-without-repeating-characters | 无重复字符的最长子串 | medium | 哈希表, 字符串, 滑动窗口 | 输出长度 |
| 9 | find-all-anagrams-in-a-string | 找到字符串中所有字母异位词 | medium | 哈希表, 字符串, 滑动窗口 | 输出起始下标数组 |
| 10 | subarray-sum-equals-k | 和为 K 的子数组 | medium | 数组, 哈希表, 前缀和 | |
| 11 | sliding-window-maximum | 滑动窗口最大值 | hard | 队列, 数组, 滑动窗口, 单调队列 | |
| 12 | minimum-window-substring | 最小覆盖子串 | hard | 哈希表, 字符串, 滑动窗口 | 无解输出空行 |
| 13 | maximum-subarray | 最大子数组和 | medium | 数组, 分治, DP | |
| 14 | merge-intervals | 合并区间 | medium | 数组, 排序 | 每行一个区间 `l r` |
| 15 | rotate-array | 轮转数组 | medium | 数组, 数学, 双指针 | 输出轮转后数组 |
| 16 | product-of-array-except-self | 除自身以外数组的乘积 | medium | 数组, 前缀和 | |
| 17 | first-missing-positive | 缺失的第一个正数 | hard | 数组, 哈希表 | |
| 18 | set-matrix-zeroes | 矩阵置零 | medium | 数组, 哈希表, 矩阵 | 输出置零后矩阵 |
| 19 | spiral-matrix | 螺旋矩阵 | medium | 矩阵, 数组, 模拟 | |
| 20 | rotate-image | 旋转图像 | medium | 数组, 数学, 矩阵 | 输出旋转后矩阵 |
| 21 | search-a-2d-matrix-ii | 搜索二维矩阵 II | medium | 数组, 二分, 矩阵 | bool |
| 22 | intersection-of-two-linked-lists | 相交链表 | easy | 哈希表, 链表, 双指针 | 输入: 两链表值序列+相交位置（题面自定义并写清）；输出相交节点值或 -1 |
| 23 | reverse-linked-list | 反转链表 | easy | 递归, 链表 | |
| 24 | palindrome-linked-list | 回文链表 | easy | 栈, 递归, 链表, 双指针 | bool |
| 25 | linked-list-cycle | 环形链表 | easy | 哈希表, 链表, 双指针 | 输入加一行 pos（环入口下标，-1 无环）；bool |
| 26 | linked-list-cycle-ii | 环形链表 II | medium | 哈希表, 链表, 双指针 | 输出入环节点值或 -1 |
| 27 | merge-two-sorted-lists | 合并两个有序链表 | easy | 递归, 链表 | |
| 28 | add-two-numbers | 两数相加 | medium | 递归, 链表, 数学 | |
| 29 | remove-nth-node-from-end-of-list | 删除链表的倒数第 N 个结点 | medium | 链表, 双指针 | |
| 30 | swap-nodes-in-pairs | 两两交换链表中的节点 | medium | 递归, 链表 | |
| 31 | reverse-nodes-in-k-group | K 个一组翻转链表 | hard | 递归, 链表 | |
| 32 | copy-list-with-random-pointer | 随机链表的复制 | medium | 哈希表, 链表 | 输入: n + 每行 `val randomIndex`(-1 表 null)；输出同格式 |
| 33 | sort-list | 排序链表 | medium | 链表, 双指针, 分治, 排序 | |
| 34 | merge-k-sorted-lists | 合并 K 个升序链表 | hard | 链表, 分治, 堆 | 输入: k + k 个链表 |
| 35 | lru-cache | LRU 缓存 | medium | 设计, 哈希表, 链表, 双向链表 | 操作序列题 |
| 36 | binary-tree-inorder-traversal | 二叉树的中序遍历 | easy | 栈, 树, DFS | |
| 37 | maximum-depth-of-binary-tree | 二叉树的最大深度 | easy | 树, DFS, BFS | |
| 38 | invert-binary-tree | 翻转二叉树 | easy | 树, DFS, BFS | 输出翻转后层序 |
| 39 | symmetric-tree | 对称二叉树 | easy | 树, DFS, BFS | bool |
| 40 | diameter-of-binary-tree | 二叉树的直径 | easy | 树, DFS | |
| 41 | binary-tree-level-order-traversal | 二叉树的层序遍历 | medium | 树, BFS | 每层一行 |
| 42 | convert-sorted-array-to-binary-search-tree | 将有序数组转换为二叉搜索树 | easy | 树, BST, 分治 | 输出层序（平衡唯一） |
| 43 | validate-binary-search-tree | 验证二叉搜索树 | medium | 树, DFS, BST | bool |
| 44 | kth-smallest-element-in-a-bst | 二叉搜索树中第 K 小的元素 | medium | 树, DFS, BST | |
| 45 | binary-tree-right-side-view | 二叉树的右视图 | medium | 树, DFS, BFS | |
| 46 | flatten-binary-tree-to-linked-list | 二叉树展开为链表 | medium | 栈, 树, DFS, 链表 | 输出展开后先序序列 |
| 47 | construct-binary-tree-from-preorder-and-inorder-traversal | 从前序与中序遍历序列构造二叉树 | medium | 树, 数组, 哈希表, 分治 | 输出层序 |
| 48 | path-sum-iii | 路径总和 III | medium | 树, DFS, 前缀和 | |
| 49 | lowest-common-ancestor-of-a-binary-tree | 二叉树的最近公共祖先 | medium | 树, DFS | 输入加 p、q 两值；输出 LCA 值 |
| 50 | binary-tree-maximum-path-sum | 二叉树中的最大路径和 | hard | 树, DFS, DP | |
| 51 | number-of-islands | 岛屿数量 | medium | DFS, BFS, 并查集, 矩阵 | 矩阵元素 0/1 |
| 52 | rotting-oranges | 腐烂的橘子 | medium | BFS, 数组, 矩阵 | |
| 53 | course-schedule | 课程表 | medium | DFS, BFS, 图, 拓扑排序 | bool |
| 54 | implement-trie-prefix-tree | 实现 Trie (前缀树) | medium | 设计, 字典树, 哈希表, 字符串 | 操作序列题 |
| 55 | permutations | 全排列 | medium | 数组, 回溯 | 多解字典序 |
| 56 | subsets | 子集 | medium | 位运算, 数组, 回溯 | 每行一个子集（升序），按 (长度,字典序) 排序 |
| 57 | letter-combinations-of-a-phone-number | 电话号码的字母组合 | medium | 哈希表, 字符串, 回溯 | 多解字典序；空输入输出空 |
| 58 | combination-sum | 组合总和 | medium | 数组, 回溯 | 每行一个组合（升序），组间字典序 |
| 59 | generate-parentheses | 括号生成 | medium | 字符串, DP, 回溯 | 多解字典序 |
| 60 | word-search | 单词搜索 | medium | 数组, 字符串, 回溯, 矩阵 | bool |
| 61 | palindrome-partitioning | 分割回文串 | medium | 字符串, DP, 回溯 | 每行一种分割（空格分隔各段），按字典序 |
| 62 | n-queens | N 皇后 | hard | 数组, 回溯 | 输出方案总数 |
| 63 | search-insert-position | 搜索插入位置 | easy | 数组, 二分查找 | |
| 64 | search-a-2d-matrix | 搜索二维矩阵 | medium | 数组, 二分, 矩阵 | bool |
| 65 | find-first-and-last-position-of-element-in-sorted-array | 在排序数组中查找元素的第一个和最后一个位置 | medium | 数组, 二分查找 | 输出两个下标 |
| 66 | search-in-rotated-sorted-array | 搜索旋转排序数组 | medium | 数组, 二分查找 | 输出下标或 -1 |
| 67 | find-minimum-in-rotated-sorted-array | 寻找旋转排序数组中的最小值 | medium | 数组, 二分查找 | |
| 68 | median-of-two-sorted-arrays | 寻找两个正序数组的中位数 | hard | 数组, 二分, 分治 | 保留 1 位小数 |
| 69 | valid-parentheses | 有效的括号 | easy | 栈, 字符串 | bool |
| 70 | min-stack | 最小栈 | medium | 栈, 设计 | 操作序列题 |
| 71 | decode-string | 字符串解码 | medium | 栈, 递归, 字符串 | |
| 72 | daily-temperatures | 每日温度 | medium | 栈, 数组, 单调栈 | |
| 73 | largest-rectangle-in-histogram | 柱状图中最大的矩形 | hard | 栈, 数组, 单调栈 | |
| 74 | kth-largest-element-in-an-array | 数组中的第 K 个最大元素 | medium | 数组, 分治, 快选, 排序, 堆 | |
| 75 | top-k-frequent-elements | 前 K 个高频元素 | medium | 数组, 哈希表, 分治, 堆, 排序 | 按频次降序，同频次按值升序 |
| 76 | find-median-from-data-stream | 数据流的中位数 | hard | 设计, 双指针, 排序, 堆 | 操作序列题；中位数保留 1 位小数 |
| 77 | best-time-to-buy-and-sell-stock | 买卖股票的最佳时机 | easy | 数组, DP | |
| 78 | jump-game | 跳跃游戏 | medium | 贪心, 数组, DP | bool |
| 79 | jump-game-ii | 跳跃游戏 II | medium | 贪心, 数组, DP | |
| 80 | partition-labels | 划分字母区间 | medium | 贪心, 哈希表, 双指针, 字符串 | |
| 81 | climbing-stairs | 爬楼梯 | easy | 记忆化搜索, 数学, DP | |
| 82 | pascals-triangle | 杨辉三角 | easy | 数组, DP | 每行一层 |
| 83 | house-robber | 打家劫舍 | medium | 数组, DP | |
| 84 | perfect-squares | 完全平方数 | medium | BFS, 数学, DP | |
| 85 | coin-change | 零钱兑换 | medium | BFS, 数组, DP | 不可凑输出 -1 |
| 86 | word-break | 单词拆分 | medium | 字典树, 记忆化, 哈希表, 字符串, DP | bool |
| 87 | longest-increasing-subsequence | 最长递增子序列 | medium | 数组, 二分, DP | |
| 88 | maximum-product-subarray | 乘积最大子数组 | medium | 数组, DP | |
| 89 | partition-equal-subset-sum | 分割等和子集 | medium | 数组, DP | bool |
| 90 | longest-valid-parentheses | 最长有效括号 | hard | 栈, 字符串, DP | |
| 91 | unique-paths | 不同路径 | medium | 数学, DP, 组合数学 | |
| 92 | minimum-path-sum | 最小路径和 | medium | 数组, DP, 矩阵 | |
| 93 | longest-palindromic-substring | 最长回文子串 | medium | 双指针, 字符串, DP | 多个最短则输出字典序最小者 |
| 94 | longest-common-subsequence | 最长公共子序列 | medium | 字符串, DP | 输出长度 |
| 95 | edit-distance | 编辑距离 | medium | 字符串, DP | |
| 96 | single-number | 只出现一次的数字 | easy | 位运算, 数组 | |
| 97 | majority-element | 多数元素 | easy | 数组, 哈希表, 分治, 计数, 排序 | |
| 98 | sort-colors | 颜色分类 | medium | 数组, 双指针, 排序 | 输出排序后数组 |
| 99 | next-permutation | 下一个排列 | medium | 数组, 双指针 | 输出下一排列数组 |
| 100 | find-the-duplicate-number | 寻找重复数 | medium | 位运算, 数组, 双指针, 二分 | |
