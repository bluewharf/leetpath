## 题目描述

中位数是有序整数列表中的中间值。如果列表长度为奇数，中位数是排序后正中间的那个数；如果长度为偶数，则没有唯一的中间值，中位数是中间两个数的平均值。

- 例如 `arr = [2, 3, 4]` 的中位数是 `3`。
- 例如 `arr = [2, 3]` 的中位数是 `(2 + 3) / 2 = 2.5`。

请实现 `MedianFinder` 类，从数据流中动态维护中位数：

- `MedianFinder()` 初始化 `MedianFinder` 对象。
- `void addNum(int num)` 将整数 `num` 加入数据结构。
- `double findMedian()` 返回当前所有元素的中位数。

## 输入格式

第一行一个整数 `q`，表示操作数。

随后 `q` 行，每行一个操作，操作名与参数空格分隔。操作集合如下：

- `MedianFinder`：初始化数据结构。保证是第一条操作，且全程只出现一次。
- `addNum x`：将整数 `x` 加入数据流。
- `findMedian`：查询当前中位数。保证调用时数据流中至少已有一个数。

## 输出格式

对每个操作按输入顺序各输出一行：

- `MedianFinder` 与 `addNum` 无返回值，输出 `null`。
- `findMedian` 输出当前中位数，**保留 1 位小数**（例如 `2.0`、`1.5`）。

## 样例

### 样例 1

输入：

```text
6
MedianFinder
addNum 1
addNum 2
findMedian
addNum 3
findMedian
```

输出：

```text
null
null
null
1.5
null
2.0
```

说明：依次加入 `1`、`2` 后，有序序列为 `[1, 2]`，中位数为 `1.5`；再加入 `3` 后为 `[1, 2, 3]`，中位数为 `2.0`。

### 样例 2

输入：

```text
5
MedianFinder
addNum 1
findMedian
addNum 2
findMedian
```

输出：

```text
null
null
1.0
null
1.5
```

## 提示（数据范围）

- `-10^5 <= num <= 10^5`
- `1 <= q <= 2000`
- 第一个操作一定是 `MedianFinder`，且全程只出现一次
- 调用 `findMedian` 前至少已执行一次 `addNum`
