## 题目描述

**Trie**（发音类似 "try"）或者说 **前缀树** 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。

请你实现 `Trie` 类：

- `Trie()` 初始化前缀树对象。
- `void insert(String word)` 向前缀树中插入字符串 `word`。
- `boolean search(String word)` 如果字符串 `word` 在前缀树中，返回 `true`（即，在检索之前已经插入）；否则，返回 `false`。
- `boolean startsWith(String prefix)` 如果之前已经插入的字符串 `word` 的前缀之一为 `prefix`，返回 `true`；否则，返回 `false`。

## 输入格式

第一行一个整数 `q`，表示操作数。

随后 `q` 行，每行一个操作，操作名与参数空格分隔。操作集合如下：

- `Trie`：初始化前缀树。保证是第一条操作，且全程只出现一次。
- `insert word`：插入字符串 `word`。
- `search word`：查询字符串 `word` 是否已完整插入。
- `startsWith prefix`：查询是否存在以 `prefix` 为前缀的已插入字符串。

## 输出格式

对每个操作按输入顺序各输出一行：

- `Trie` 与 `insert` 无返回值，输出 `null`。
- `search` 与 `startsWith` 输出 `true` 或 `false`（小写）。

## 样例

### 样例 1

输入：

```text
7
Trie
insert apple
search apple
search app
startsWith app
insert app
search app
```

输出：

```text
null
null
true
false
true
null
true
```

### 样例 2

输入：

```text
6
Trie
insert a
search a
search b
startsWith a
startsWith b
```

输出：

```text
null
null
true
false
true
false
```

## 提示（数据范围）

- `1 <= word.length, prefix.length <= 2000`
- `word` 和 `prefix` 仅由小写英文字母组成
- `1 <= q <= 2000`
- 第一个操作一定是 `Trie`，且全程只出现一次
