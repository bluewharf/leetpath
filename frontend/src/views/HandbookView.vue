<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Handbook & Roadmap</div>
        <h1 class="display">算法新手村与速查手册</h1>
      </div>
      <div class="head-stats">
        <div class="stat">
          <span class="num accent">4</span>
          <span class="lbl">顶流笔记</span>
        </div>
        <div class="stat">
          <span class="num">7</span>
          <span class="lbl">必背模板</span>
        </div>
        <div class="stat">
          <span class="num">Py / C++</span>
          <span class="lbl">双语对齐</span>
        </div>
      </div>
    </div>

    <!-- 导航选项卡 -->
    <div class="handbook-nav-tabs">
      <button :class="{ active: currentTab === 'links' }" @click="currentTab = 'links'">
        🌟 顶流开源笔记导航
      </button>
      <button :class="{ active: currentTab === 'complexity' }" @click="currentTab = 'complexity'">
        🧮 数据规模与复杂度速查
      </button>
      <button :class="{ active: currentTab === 'syntax' }" @click="currentTab = 'syntax'">
        ⚡ Python ⇋ C++ 语法对齐
      </button>
      <button :class="{ active: currentTab === 'templates' }" @click="currentTab = 'templates'">
        🎯 7 大核心算法通用模板
      </button>
    </div>

    <!-- 模块 1: 顶流开源笔记推荐 -->
    <section v-if="currentTab === 'links'" class="handbook-section">
      <div class="curated-grid">
        <a
          v-for="item in CURATED_RESOURCES"
          :key="item.title"
          :href="item.url"
          target="_blank"
          rel="noopener"
          class="card curated-card"
        >
          <div class="curated-top">
            <span class="curated-badge">{{ item.badge }}</span>
            <span class="curated-star">{{ item.stars }}</span>
          </div>
          <h3 class="curated-title">{{ item.title }}</h3>
          <p class="curated-desc">{{ item.desc }}</p>
          <div class="curated-footer">
            <span class="curated-tag">{{ item.tag }}</span>
            <span class="curated-link">前往阅读 ↗</span>
          </div>
        </a>
      </div>
    </section>

    <!-- 模块 2: 数据规模倒推法则 -->
    <section v-if="currentTab === 'complexity'" class="handbook-section">
      <div class="card rule-card">
        <h2>⏱️ 数据规模与时间复杂度倒推法则（面试秒出思路）</h2>
        <p class="rule-intro">
          在算法面试和 OJ 中，<strong>看一眼题目给出的数据范围 $n$，就能直接倒推本题允许的理论最大时间复杂度</strong>（以单核 1 秒运算 $10^8$ 次为基准）：
        </p>

        <div class="table-wrap">
          <table class="handbook-table">
            <thead>
              <tr>
                <th>数据规模 $n$</th>
                <th>允许的最大时间复杂度</th>
                <th>常见算法与思路提示</th>
                <th>典型面试题型</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in COMPLEXITY_RULES" :key="r.range">
                <td class="mono bold accent-cell">{{ r.range }}</td>
                <td class="mono bold">{{ r.complexity }}</td>
                <td>{{ r.algorithms }}</td>
                <td style="color:var(--text-dim)">{{ r.examples }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 模块 3: Python 3 ⇋ C++ 20 语法对齐 -->
    <section v-if="currentTab === 'syntax'" class="handbook-section">
      <div class="card rule-card">
        <h2>⚡ Python 3 ⇋ C++ 20 高频数据结构与常用内置方法对照</h2>
        <p class="rule-intro">
          结对刷题或双语学习时随手查阅，涵盖竞赛与面试中最常用的标准库操作：
        </p>

        <div class="table-wrap">
          <table class="handbook-table">
            <thead>
              <tr>
                <th>场景 / 数据结构</th>
                <th>Python 3 写法</th>
                <th>C++ 20 (STL) 写法</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in SYNTAX_ALIGN" :key="s.name">
                <td class="bold">{{ s.name }}</td>
                <td class="mono code-cell">{{ s.python }}</td>
                <td class="mono code-cell">{{ s.cpp }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ACM 模式极速 I/O 模板 -->
        <h3 style="margin-top:28px;font-size:16px">🚀 ACM 模式极速 I/O 输入输出防 TLE 模板</h3>
        <div class="io-templates-grid">
          <div class="io-temp-box">
            <div class="io-temp-head">
              <span>Python 3 极速读取</span>
              <button class="btn btn-xs" @click="copy(PY_IO_CODE)">复制</button>
            </div>
            <pre class="mono io-pre">{{ PY_IO_CODE }}</pre>
          </div>

          <div class="io-temp-box">
            <div class="io-temp-head">
              <span>C++ 20 关同步极速 I/O</span>
              <button class="btn btn-xs" @click="copy(CPP_IO_CODE)">复制</button>
            </div>
            <pre class="mono io-pre">{{ CPP_IO_CODE }}</pre>
          </div>
        </div>
      </div>
    </section>

    <!-- 模块 4: 7 大核心算法通用骨架模板 -->
    <section v-if="currentTab === 'templates'" class="handbook-section">
      <div class="template-layout">
        <!-- 侧边模板列表 -->
        <div class="template-menu card">
          <button
            v-for="(t, idx) in TEMPLATES"
            :key="t.title"
            class="template-menu-item"
            :class="{ active: selectedTemplateIdx === idx }"
            @click="selectedTemplateIdx = idx"
          >
            <span class="tpl-idx">#0{{ idx + 1 }}</span>
            <span class="tpl-name">{{ t.title }}</span>
          </button>
        </div>

        <!-- 模板代码展示区 -->
        <div class="template-content card" v-if="currentTemplate">
          <div class="tpl-header">
            <div>
              <h2>{{ currentTemplate.title }}</h2>
              <p class="tpl-desc">{{ currentTemplate.desc }}</p>
            </div>
            <div class="tpl-actions">
              <div class="lang-switch-pills">
                <button
                  :class="{ active: tplLang === 'python3' }"
                  @click="tplLang = 'python3'"
                >
                  Python 3
                </button>
                <button
                  :class="{ active: tplLang === 'cpp' }"
                  @click="tplLang = 'cpp'"
                >
                  C++ 20
                </button>
              </div>
              <button class="btn btn-sm btn-primary" @click="copy(currentTemplate[tplLang])">
                📋 复制完整模板
              </button>
            </div>
          </div>

          <div class="tpl-code-block">
            <pre class="mono">{{ currentTemplate[tplLang] }}</pre>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useToast } from '../stores/toast'
import { useLangPref } from '../stores/pref'

const toast = useToast()
const { langPref } = useLangPref()
const currentTab = ref<'links' | 'complexity' | 'syntax' | 'templates'>('links')
const selectedTemplateIdx = ref(0)
const tplLang = ref<'python3' | 'cpp'>(langPref.value)

watch(langPref, (newLang) => {
  tplLang.value = newLang
})

function copy(text: string) {
  navigator.clipboard.writeText(text)
  toast.success('模板代码已复制到剪贴板')
}

const CURATED_RESOURCES = [
  {
    title: 'Hello 算法 (Hello Algo)',
    url: 'https://www.hello-algo.com/',
    badge: '🌟 动画图解顶流',
    stars: '100k+ Stars',
    desc: '全网零基础入门最友好的开源算法教程！动画生动展示数据结构与算法执行全过程，覆盖 Python/C++/Java/Go 全语言。',
    tag: '零基础 · 图解 · 交互式学习',
  },
  {
    title: '代码随想录 (Programmer Carl)',
    url: 'https://programmercarl.com/',
    badge: '🏆 校招面试必读',
    stars: '50k+ Stars',
    desc: '国内程序员校招刷题人手一本的求职宝典！按专题（二叉树、动态规划五步法、回溯、双指针）归纳总结通用做题套路。',
    tag: '专题刷题 · 模板总结 · 面试高频',
  },
  {
    title: 'labuladong 的算法笔记',
    url: 'https://labuladong.online/',
    badge: '🧠 算法框架思维',
    stars: '120k+ Stars',
    desc: '主打手把手拆解通用算法框架，将滑动窗口、二分查找、二叉树遍历框架化，掌握一个框架轻松秒杀一整类算法题。',
    tag: '框架思维 · 递归模式 · 核心模板',
  },
  {
    title: 'OI Wiki 算法竞赛百科',
    url: 'https://oi-wiki.org/',
    badge: '📚 权威算法百科',
    stars: '30k+ Stars',
    desc: '由算法竞赛圈共同维护的最权威中文算法百科全书，数学推导严谨，涵盖从基础数据结构到高级图论算法的全部细节。',
    tag: '百科全书 · 严谨推导 · 竞赛进阶',
  },
]

const COMPLEXITY_RULES = [
  {
    range: 'n ≤ 10 ~ 20',
    complexity: 'O(2ⁿ) 或 O(n!)',
    algorithms: '指数级回溯爆搜、全排列枚举、状态压缩 DP',
    examples: 'N 皇后、全排列、子集划分、旅行商问题',
  },
  {
    range: 'n ≤ 100',
    complexity: 'O(n³)',
    algorithms: '三重循环枚举、Floyd 多源最短路、区间 DP',
    examples: '矩阵连乘、戳气球、多源最短路径',
  },
  {
    range: 'n ≤ 1,000',
    complexity: 'O(n²)',
    algorithms: '双重循环、二维动态规划、稠密图 Dijkstra',
    examples: '最长公共子序列、编辑距离、打家劫舍 II',
  },
  {
    range: 'n ≤ 10⁵ ~ 10⁶',
    complexity: 'O(n log n) 或 O(n)',
    algorithms: '快速排序/归并排序、堆/二分、双指针、滑动窗口、单调栈/单调队列',
    examples: '三数之和、接雨水、滑动窗口最大值、最长上升子序列',
  },
  {
    range: 'n ≥ 10⁹',
    complexity: 'O(log n) 或 O(1)',
    algorithms: '二分查找、快速幂、数论公式推导、位运算',
    examples: 'Pow(x, n)、两数相除、只出现一次的数字',
  },
]

const SYNTAX_ALIGN = [
  {
    name: '双端队列 (Deque)',
    python: 'from collections import deque\nq = deque()\nq.append(x); q.popleft()',
    cpp: '#include <deque>\nstd::deque<int> q;\nq.push_back(x); q.pop_front();',
  },
  {
    name: '大顶堆 (Max Heap)',
    python: 'import heapq\nh = []\nheapq.heappush(h, -x)\nval = -heapq.heappop(h)',
    cpp: '#include <queue>\nstd::priority_queue<int> pq;\npq.push(x);\nval = pq.top(); pq.pop();',
  },
  {
    name: '小顶堆 (Min Heap)',
    python: 'import heapq\nh = []\nheapq.heappush(h, x)\nval = heapq.heappop(h)',
    cpp: 'std::priority_queue<int, vector<int>, greater<int>> pq;\npq.push(x);\nval = pq.top(); pq.pop();',
  },
  {
    name: '哈希计数器 (Counter)',
    python: 'from collections import Counter\ncnt = Counter(nums)\n# 自动计数',
    cpp: '#include <unordered_map>\nstd::unordered_map<int, int> cnt;\nfor (int x : nums) cnt[x]++;',
  },
  {
    name: '二分查找 (下界 ≥ x)',
    python: 'import bisect\nidx = bisect.bisect_left(nums, target)',
    cpp: '#include <algorithm>\nauto it = std::lower_bound(nums.begin(), nums.end(), target);\nint idx = it - nums.begin();',
  },
  {
    name: '自定义排序 (降序/多键)',
    python: 'nums.sort(key=lambda x: (x[0], -x[1]))',
    cpp: 'std::sort(nums.begin(), nums.end(), [](const auto& a, const auto& b) {\n    return a[0] != b[0] ? a[0] < b[0] : a[1] > b[1];\n});',
  },
]

const PY_IO_CODE = `import sys

def solve():
    # 一次性读入所有数据，极速切片
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # 示例：读入一个整数 n
    it = iter(input_data)
    n = int(next(it))
    nums = [int(next(it)) for _ in range(n)]
    
    # 业务解题逻辑
    res = sum(nums)
    print(res)

if __name__ == "__main__":
    solve()`

const CPP_IO_CODE = `#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    // 关闭同步流加速，避免大规模输入 TLE
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (cin >> n) {
        vector<int> nums(n);
        for (int i = 0; i < n; ++i) {
            cin >> nums[i];
        }
        // 业务解题逻辑
        long long res = 0;
        for (int x : nums) res += x;
        cout << res << "\\n";
    }
    return 0;
}`

const TEMPLATES = [
  {
    title: '二分查找 (Binary Search)',
    desc: '左右闭区间统一模板，杜绝死循环与边界越界错误。',
    python3: `def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # 未找到`,
    cpp: `int binarySearch(const vector<int>& nums, int target) {
    int left = 0, right = static_cast<int>(nums.size()) - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}`,
  },
  {
    title: '滑动窗口 (Sliding Window)',
    desc: '双指针快慢指针同向移动，维护区间动态合法状态。',
    python3: `def sliding_window(s: str) -> int:
    from collections import defaultdict
    window = defaultdict(int)
    left = right = 0
    ans = 0
    
    while right < len(s):
        c = s[right]
        right += 1
        window[c] += 1
        
        # 当窗口需要收缩时
        while window[c] > 1: # 满足收缩条件
            d = s[left]
            left += 1
            window[d] -= 1
            
        ans = max(ans, right - left)
    return ans`,
    cpp: `int slidingWindow(const string& s) {
    unordered_map<char, int> window;
    int left = 0, right = 0, ans = 0;
    while (right < s.size()) {
        char c = s[right++];
        window[c]++;
        
        while (window[c] > 1) {
            char d = s[left++];
            window[d]--;
        }
        ans = max(ans, right - left);
    }
    return ans;
}`,
  },
  {
    title: '二叉树递归遍历 (Tree Traversal)',
    desc: '标准前/中/后序统一递归框架与叶节点递归出口。',
    python3: `class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def traverse(root: TreeNode | None):
    if not root:
        return
    # 前序位置: print(root.val)
    traverse(root.left)
    # 中序位置: print(root.val)
    traverse(root.right)
    # 后序位置: print(root.val)`,
    cpp: `struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void traverse(TreeNode* root) {
    if (!root) return;
    // 前序位置
    traverse(root->left);
    // 中序位置
    traverse(root->right);
    // 后序位置
}`,
  },
  {
    title: '回溯搜索与剪枝 (Backtracking)',
    desc: '路径选择与撤销选择通用框架，应对排列组合与子集问题。',
    python3: `def backtrack(choices: list[int], path: list[int], res: list[list[int]], used: list[bool]):
    # 满足终止条件
    if len(path) == len(choices):
        res.append(path[:])
        return
        
    for i in range(len(choices)):
        if used[i]:
            continue
        # 剪枝判断...
        
        # 做出选择
        used[i] = True
        path.append(choices[i])
        
        backtrack(choices, path, res, used)
        
        # 撤销选择
        path.pop()
        used[i] = False`,
    cpp: `void backtrack(const vector<int>& nums, vector<int>& path, vector<vector<int>>& res, vector<bool>& used) {
    if (path.size() == nums.size()) {
        res.push_back(path);
        return;
    }
    for (size_t i = 0; i < nums.size(); ++i) {
        if (used[i]) continue;
        used[i] = true;
        path.push_back(nums[i]);
        
        backtrack(nums, path, res, used);
        
        path.pop_back();
        used[i] = false;
    }
}`,
  },
  {
    title: '并查集 (Union-Find 带路径压缩)',
    desc: '高效处理图的连通分量与环路检测。',
    python3: `class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.count = n
        
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # 路径压缩
        return self.parent[x]
        
    def union(self, x: int, y: int) -> bool:
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        self.parent[root_x] = root_y
        self.count -= 1
        return True`,
    cpp: `class UnionFind {
public:
    vector<int> parent;
    int count;
    UnionFind(int n) : parent(n), count(n) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        parent[rx] = ry;
        count--;
        return true;
    }
};`,
  },
  {
    title: '单调栈 (Monotonic Stack)',
    desc: 'O(N) 线性时间快速找到数组中每个元素左/右第一个更大或更小元素。',
    python3: `def next_greater_element(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack = []  # 存索引，单调递减
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            res[idx] = nums[i]
        stack.append(i)
    return res`,
    cpp: `vector<int> nextGreaterElement(const vector<int>& nums) {
    int n = nums.size();
    vector<int> res(n, -1);
    vector<int> st; // 单调递减栈
    
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && nums[i] > nums[st.back()]) {
            res[st.back()] = nums[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    return res;
}`,
  },
  {
    title: '拓扑排序 (Topological Sort / Kahn 算法)',
    desc: '检测有向图环路与确定依赖任务执行顺序。',
    python3: `def topological_sort(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    from collections import deque, defaultdict
    in_degree = [0] * num_courses
    adj = defaultdict(list)
    
    for cur, pre in prerequisites:
        adj[pre].append(cur)
        in_degree[cur] += 1
        
    q = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []
    
    while q:
        node = q.popleft()
        order.append(node)
        for nxt in adj[node]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                q.append(nxt)
                
    return order if len(order) == num_courses else []`,
    cpp: `vector<int> topologicalSort(int numCourses, const vector<vector<int>>& prerequisites) {
    vector<int> inDegree(numCourses, 0);
    vector<vector<int>> adj(numCourses);
    for (const auto& p : prerequisites) {
        adj[p[1]].push_back(p[0]);
        inDegree[p[0]]++;
    }
    queue<int> q;
    for (int i = 0; i < numCourses; ++i) {
        if (inDegree[i] == 0) q.push(i);
    }
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    return order.size() == numCourses ? order : vector<int>{};
}`,
  },
]

const currentTemplate = computed(() => TEMPLATES[selectedTemplateIdx.value])
</script>
