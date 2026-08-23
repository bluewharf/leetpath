## 题目描述

设计一个支持 `push`、`pop`、`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类：

- `MinStack()` 初始化堆栈对象。
- `void push(int val)` 将元素 `val` 推入堆栈。
- `void pop()` 删除堆栈顶部的元素。
- `int top()` 获取堆栈顶部的元素。
- `int getMin()` 获取堆栈中的最小元素。

## 输入格式

第一行一个整数 `q`，表示操作数。

随后 `q` 行，每行一个操作，操作名与参数空格分隔。操作集合如下：

- `MinStack`：初始化最小栈。保证是第一条操作，且全程只出现一次。
- `push val`：将整数 `val` 压入栈顶。
- `pop`：弹出栈顶元素。保证调用时栈非空。
- `top`：查询栈顶元素。保证调用时栈非空。
- `getMin`：查询当前栈中的最小元素。保证调用时栈非空。

## 输出格式

对每个操作按输入顺序各输出一行：

- `MinStack`、`push`、`pop` 无返回值，输出 `null`。
- `top` 输出栈顶整数。
- `getMin` 输出当前栈中的最小整数。

## 样例

### 样例 1

输入：

```text
8
MinStack
push -2
push 0
push -3
getMin
pop
top
getMin
```

输出：

```text
null
null
null
null
-3
null
0
-2
```

### 样例 2

输入：

```text
5
MinStack
push 1
push 2
top
getMin
```

输出：

```text
null
null
null
2
1
```

## 提示（数据范围）

- `1 <= q <= 500`
- `-2^{31} <= val <= 2^{31} - 1`
- 第一个操作一定是 `MinStack`
- `pop`、`top`、`getMin` 仅在栈非空时调用
