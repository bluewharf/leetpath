"""把力扣函数写法套上 ACM 读入/输出。用户只写 class Solution / 设计类。"""

from __future__ import annotations

import json
import re
from typing import Any



PY_HINT = {
    "int": "int",
    "vec": "List[int]",
    "vec2": "List[List[int]]",
    "intervals": "List[List[int]]",
    "str": "str",
    "strs": "List[str]",
    "listnode": "Optional[ListNode]",
    "listnodes": "List[Optional[ListNode]]",
    "tree": "Optional[TreeNode]",
    "grid01": "List[List[str]]",
    "board": "List[List[str]]",
    "cycle": "Optional[ListNode]",
    "random": "Optional[Node]",
}

PY_RET = {
    "int": "int",
    "float": "float",
    "bool": "bool",
    "str": "str",
    "vec": "List[int]",
    "vec2": "List[List[int]]",
    "intervals": "List[List[int]]",
    "listnode": "Optional[ListNode]",
    "tree": "Optional[TreeNode]",
    "lines": "List[List[int]]",
    "perms": "List[List[int]]",
    "subsets": "List[List[int]]",
    "str_lines": "List[str]",
    "str_lines_space": "List[List[str]]",
    "groups": "List[List[str]]",
    "void_vec": "None",
    "void_mat": "None",
    "void_tree": "None",
    "nqueens": "List[List[str]]",
    "pascal": "List[List[int]]",
    "random": "Optional[Node]",
    "cycle_val": "Optional[ListNode]",
    "lca_val": "Optional[TreeNode]",
    "levels": "List[List[int]]",
}

CPP_TYPE = {
    "int": "int",
    "vec": "vector<int>",
    "vec2": "vector<vector<int>>",
    "intervals": "vector<vector<int>>",
    "str": "string",
    "strs": "vector<string>",
    "listnode": "ListNode*",
    "listnodes": "vector<ListNode*>",
    "tree": "TreeNode*",
    "grid01": "vector<vector<char>>",
    "board": "vector<vector<char>>",
    "cycle": "ListNode*",
    "random": "Node*",
    "float": "double",
    "bool": "bool",
    "void": "void",
}

CTOR_ARG_NAMES = {
    "LRUCache": ["capacity"],
}

METHOD_ARG_NAMES = {
    "push": ["val"],
    "get": ["key"],
    "put": ["key", "value"],
    "insert": ["word"],
    "search": ["word"],
    "startsWith": ["prefix"],
    "addNum": ["num"],
}

_LISTNODE_PY = """\
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
"""

_TREE_PY = """\
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
"""

_NODE_PY = """\
# Definition for a Node.
# class Node:
#     def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
#         self.val = int(x)
#         self.next = next
#         self.random = random
"""

_LISTNODE_CPP = """\
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
"""

_TREE_CPP = """\
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
"""

_NODE_CPP = """\
/**
 * Definition for a Node.
 * class Node {
 * public:
 *     int val;
 *     Node* next;
 *     Node* random;
 *     Node(int _val) {
 *         val = _val;
 *         next = NULL;
 *         random = NULL;
 *     }
 * };
 */
"""


def _needs_types(spec: dict[str, Any]) -> set[str]:
    kinds: set[str] = set()
    params = spec.get("params") or []
    ret = spec.get("returns")
    blob = params + ([ret] if ret else [])
    for p in blob:
        if p in {"listnode", "listnodes", "cycle", "intersect", "cycle_val"}:
            kinds.add("listnode")
        if p in {"tree", "lca", "lca_val", "void_tree"}:
            kinds.add("tree")
        if p in {"random"}:
            kinds.add("random")
    if spec.get("kind") == "design":
        return kinds
    return kinds


def _py_args(spec: dict[str, Any]) -> str:
    params = spec["params"]
    names = list(spec.get("names") or [])
    if params == ["edges"]:
        return "numCourses: int, prerequisites: List[List[int]]"
    if params == ["lca"]:
        return "root: Optional[TreeNode], p: Optional[TreeNode], q: Optional[TreeNode]"
    if params == ["intersect"]:
        return "headA: Optional[ListNode], headB: Optional[ListNode]"
    args: list[str] = []
    for i, p in enumerate(params):
        name = names[i] if i < len(names) else f"arg{i}"
        args.append(f"{name}: {PY_HINT.get(p, 'object')}")
    return ", ".join(args)


def _cpp_return_type(ret: str) -> str:
    if ret in {"void_vec", "void_mat", "void_tree"}:
        return "void"
    mapping = {
        "lines": "vector<vector<int>>",
        "perms": "vector<vector<int>>",
        "subsets": "vector<vector<int>>",
        "pascal": "vector<vector<int>>",
        "levels": "vector<vector<int>>",
        "intervals": "vector<vector<int>>",
        "str_lines": "vector<string>",
        "str_lines_space": "vector<vector<string>>",
        "groups": "vector<vector<string>>",
        "nqueens": "vector<vector<string>>",
        "cycle_val": "ListNode*",
        "lca_val": "TreeNode*",
        "random": "Node*",
        "float": "double",
        "listnode": "ListNode*",
        "tree": "TreeNode*",
        "vec": "vector<int>",
        "vec2": "vector<vector<int>>",
        "str": "string",
        "bool": "bool",
        "int": "int",
    }
    return mapping.get(ret, CPP_TYPE.get(ret, "int"))


def _cpp_args(spec: dict[str, Any]) -> str:
    params = spec["params"]
    names = list(spec.get("names") or [])
    if params == ["edges"]:
        return "int numCourses, vector<vector<int>>& prerequisites"
    if params == ["lca"]:
        return "TreeNode* root, TreeNode* p, TreeNode* q"
    if params == ["intersect"]:
        return "ListNode* headA, ListNode* headB"
    args: list[str] = []
    for i, p in enumerate(params):
        name = names[i] if i < len(names) else f"arg{i}"
        ty = {
            "cycle": "ListNode*",
            "random": "Node*",
        }.get(p, CPP_TYPE.get(p, "int"))
        if p in {"vec", "vec2", "intervals", "strs", "grid01", "board", "listnodes"}:
            args.append(f"{ty}& {name}")
        else:
            args.append(f"{ty} {name}")
    return ", ".join(args)


def _py_sig(spec: dict[str, Any]) -> str:
    inner = _py_args(spec)
    ret = PY_RET.get(spec["returns"], "object")
    prefix = f"self, {inner}" if inner else "self"
    return f"    def {spec['method']}({prefix}) -> {ret}:\n        ..."


def _cpp_sig(spec: dict[str, Any]) -> str:
    rt = _cpp_return_type(spec["returns"])
    args = _cpp_args(spec)
    return f"    {rt} {spec['method']}({args}) {{\n        \n    }}"


def generate_starter(spec: dict[str, Any], language: str) -> str:
    if spec["kind"] == "design":
        return _starter_design(spec, language)
    if language == "cpp":
        comments = []
        kinds = _needs_types(spec)
        if "listnode" in kinds:
            comments.append(_LISTNODE_CPP.rstrip())
        if "tree" in kinds:
            comments.append(_TREE_CPP.rstrip())
        if "random" in kinds:
            comments.append(_NODE_CPP.rstrip())
        head = ("\n".join(comments) + "\n") if comments else ""
        return head + "class Solution {\npublic:\n" + _cpp_sig(spec) + "\n};\n"
    comments = []
    kinds = _needs_types(spec)
    if "listnode" in kinds:
        comments.append(_LISTNODE_PY.rstrip())
    if "tree" in kinds:
        comments.append(_TREE_PY.rstrip())
    if "random" in kinds:
        comments.append(_NODE_PY.rstrip())
    extra = ("\n".join(comments) + "\n\n") if comments else ""
    return (
        "from typing import List, Optional\n\n"
        + extra
        + "class Solution:\n"
        + _py_sig(spec)
        + "\n"
    )


def _starter_design(spec: dict[str, Any], language: str) -> str:
    cls = spec["class"]
    ctor = spec.get("ctor") or []
    methods = spec["methods"]
    if language == "cpp":
        lines = [f"class {cls} {{", "public:"]
        ctor_names = CTOR_ARG_NAMES.get(cls) or [f"arg{i}" for i in range(len(ctor))]
        ctor_args = ", ".join(
            f"{CPP_TYPE.get(t, 'int')} {n}" for t, n in zip(ctor, ctor_names, strict=False)
        )
        lines.append(f"    {cls}({ctor_args}) {{")
        lines.append("        ")
        lines.append("    }")
        for name, meta in methods.items():
            params = list(meta["params"])
            ret = str(meta["returns"])
            rt = "void" if ret == "void" else ("double" if ret == "float" else CPP_TYPE.get(ret, "int"))
            arg_names = METHOD_ARG_NAMES.get(name) or [f"arg{i}" for i in range(len(params))]
            args = ", ".join(
                f"{CPP_TYPE.get(t, 'int')} {n}" for t, n in zip(params, arg_names, strict=False)
            )
            lines.append("")
            lines.append(f"    {rt} {name}({args}) {{")
            lines.append("        ")
            lines.append("    }")
        lines.append("};")
        lines.append("")
        return "\n".join(lines)

    lines: list[str] = [f"class {cls}:"]
    if ctor:
        ctor_names = CTOR_ARG_NAMES.get(cls) or [f"arg{i}" for i in range(len(ctor))]
        args = ", ".join(
            f"{n}: {PY_HINT.get(t, 'int')}" for n, t in zip(ctor_names, ctor, strict=False)
        )
        lines.append(f"    def __init__(self, {args}) -> None:")
    else:
        lines.append("    def __init__(self) -> None:")
    lines.append("        ...")
    for name, meta in methods.items():
        params = list(meta["params"])
        ret = str(meta["returns"])
        rh = "None" if ret == "void" else PY_RET.get(ret, PY_HINT.get(ret, "object"))
        if ret == "bool":
            rh = "bool"
        elif ret == "int":
            rh = "int"
        elif ret == "float":
            rh = "float"
        arg_names = METHOD_ARG_NAMES.get(name) or [f"arg{i}" for i in range(len(params))]
        args = ", ".join(
            f"{an}: {PY_HINT.get(t, 'int')}" for an, t in zip(arg_names, params, strict=False)
        )
        inner = f", {args}" if args else ""
        lines.append("")
        lines.append(f"    def {name}(self{inner}) -> {rh}:")
        lines.append("        ...")
    lines.append("")
    return "\n".join(lines)


def _strip_user_main(code: str) -> str:
    lines = code.splitlines()
    out: list[str] = []
    for line in lines:
        if re.match(r"if\s+__name__\s*==", line):
            break
        out.append(line)
    return "\n".join(out).rstrip() + "\n"


_PY_PREAMBLE = """\
from __future__ import annotations

from collections import Counter, deque
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

"""

_PY_RUNTIME = r'''
import json
import sys

SPEC = json.loads(__SPEC__)
_RAW = sys.stdin.read().replace("\r\n", "\n").replace("\r", "\n")
_LINES = _RAW.split("\n")
if _LINES and _LINES[-1] == "":
    _LINES.pop()


class _Cur:
    def __init__(self):
        self.lines = _LINES
        self.li = 0
        self.buf = []

    def _fill(self):
        while not self.buf and self.li < len(self.lines):
            parts = self.lines[self.li].split()
            self.li += 1
            if parts:
                self.buf.extend(parts)

    def take_int(self):
        self._fill()
        return int(self.buf.pop(0))

    def take_tok(self):
        self._fill()
        return self.buf.pop(0)

    def take_line(self):
        if self.buf:
            s = " ".join(self.buf)
            self.buf.clear()
            return s
        if self.li < len(self.lines):
            s = self.lines[self.li]
            self.li += 1
            return s
        return ""

    def take_vec(self):
        n = self.take_int()
        return [self.take_int() for _ in range(n)]

    def take_vec2(self, as_char=False, as_grid01=False):
        m, n = self.take_int(), self.take_int()
        grid = []
        for _ in range(m):
            row = [self.take_tok() for _ in range(n)]
            if as_grid01:
                grid.append([("1" if int(x) == 1 else "0") for x in row])
            elif as_char:
                grid.append([str(x) for x in row])
            else:
                grid.append([int(x) for x in row])
        return grid

    def take_intervals(self):
        m, n = self.take_int(), self.take_int()
        arr = []
        for _ in range(m):
            a, b = self.take_int(), self.take_int()
            arr.append([a, b])
            for _skip in range(max(0, n - 2)):
                self.take_int()
        return arr

    def take_list(self):
        n = self.take_int()
        vals = [self.take_int() for _ in range(n)] if n else []
        return _build_list(vals)

    def take_tree(self):
        n = self.take_int()
        tokens = [self.take_tok() for _ in range(n)] if n else []
        return _build_tree(n, tokens)


def _build_list(vals):
    dummy = ListNode()
    cur = dummy
    nodes = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    return dummy.next, nodes


def _write_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    if not vals:
        print(0)
        return
    print(len(vals))
    print(" ".join(vals))


def _build_tree(n, tokens):
    if n == 0:
        return None

    def parse(i):
        if tokens[i] == "null":
            return None
        return TreeNode(int(tokens[i]))

    root = parse(0)
    q = deque([root])
    i = 1
    while q and i < n:
        node = q.popleft()
        if node is None:
            continue
        if i < n:
            node.left = parse(i)
            if node.left:
                q.append(node.left)
            i += 1
        if i < n:
            node.right = parse(i)
            if node.right:
                q.append(node.right)
            i += 1
    return root


def _write_tree(root):
    if root is None:
        print(0)
        return
    q = deque([root])
    tokens = []
    while q:
        node = q.popleft()
        if node is None:
            tokens.append("null")
            continue
        tokens.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    print(len(tokens))
    print(" ".join(tokens))


def _find_node(root, val):
    if root is None:
        return None
    if root.val == val:
        return root
    return _find_node(root.left, val) or _find_node(root.right, val)


def _print_int_rows(rows, mode):
    rows = [list(r) for r in (rows or [])]
    if mode != "perms":
        for r in rows:
            r.sort()
    if mode == "subsets":
        rows.sort(key=lambda s: (len(s), s))
    else:
        rows.sort()
    for row in rows:
        print(" ".join(map(str, row)))


def _print_ret(kind, val, first=None, args=None):
    if kind == "int":
        print(int(val))
    elif kind == "float":
        print(f"{float(val):.1f}")
    elif kind == "bool":
        print("true" if val else "false")
    elif kind == "str":
        print("" if val is None else val)
    elif kind == "vec":
        seq = list(val) if val is not None else []
        if SPEC.get("sort"):
            seq = sorted(seq)
        elif SPEC.get("rank") == "freq" and args:
            cnt = Counter(args[0])
            seq = sorted(seq, key=lambda x: (-cnt[x], x))
        print(" ".join(map(str, seq)))
    elif kind == "void_vec":
        print(" ".join(map(str, first or [])))
    elif kind == "void_mat":
        mat = first or []
        print(len(mat), len(mat[0]) if mat else 0)
        for row in mat:
            print(" ".join(map(str, row)))
    elif kind == "listnode":
        _write_list(val)
    elif kind == "tree":
        _write_tree(val)
    elif kind == "void_tree":
        _write_tree(first)
    elif kind in ("lines", "perms", "subsets"):
        _print_int_rows(val, kind)
    elif kind == "str_lines":
        for s in sorted(val or []):
            print(s)
    elif kind == "str_lines_space":
        rows = [list(row) for row in (val or [])]
        for r in rows:
            r.sort()
        rows.sort()
        for row in rows:
            print(" ".join(row))
    elif kind == "groups":
        rows = [sorted(row) for row in (val or [])]
        rows.sort(key=lambda g: g[0] if g else "")
        for row in rows:
            print(" ".join(row))
    elif kind == "nqueens":
        print(len(val or []))
    elif kind == "pascal":
        for row in val or []:
            print(" ".join(map(str, row)))
    elif kind == "levels":
        for row in val or []:
            print(" ".join(map(str, row)))
    elif kind == "intervals":
        for a, b in val or []:
            print(a, b)
    elif kind == "cycle_val":
        print(-1 if val is None else val.val)
    elif kind == "lca_val":
        print(val.val)
    elif kind == "random":
        if val is None:
            print(0)
            return
        arr = []
        cur = val
        while cur:
            arr.append(cur)
            cur = cur.next
        idx = {node: i for i, node in enumerate(arr)}
        print(len(arr))
        for node in arr:
            ri = idx[node.random] if node.random is not None else -1
            print(node.val, ri)
    else:
        print(val)


def _run_fn():
    cur = _Cur()
    args = []
    first_mut = None
    for kind in SPEC["params"]:
        if kind == "int":
            val = cur.take_int()
        elif kind == "vec":
            val = cur.take_vec()
        elif kind == "vec2":
            val = cur.take_vec2()
        elif kind == "intervals":
            val = cur.take_intervals()
        elif kind == "str":
            val = cur.take_line()
        elif kind == "strs":
            n = cur.take_int()
            val = [cur.take_line() for _ in range(n)]
        elif kind == "listnode":
            val, _ = cur.take_list()
        elif kind == "listnodes":
            k = cur.take_int()
            lists = []
            for _ in range(k):
                head, _ = cur.take_list()
                lists.append(head)
            val = lists
        elif kind == "tree":
            val = cur.take_tree()
        elif kind == "grid01":
            val = cur.take_vec2(as_grid01=True)
        elif kind == "board":
            val = cur.take_vec2(as_char=True)
        elif kind == "edges":
            n = cur.take_int()
            m = cur.take_int()
            cur.take_int()  # 二维数组列数，恒为 2
            prereq = [[cur.take_int(), cur.take_int()] for _ in range(m)]
            args.extend([n, prereq])
            continue
        elif kind == "cycle":
            n = cur.take_int()
            if n == 0:
                if cur.buf or cur.li < len(cur.lines):
                    try:
                        cur.take_int()
                    except Exception:
                        pass
                args.append(None)
                continue
            vals = [cur.take_int() for _ in range(n)]
            pos = cur.take_int()
            head, nodes = _build_list(vals)
            if 0 <= pos < n:
                nodes[-1].next = nodes[pos]
            args.append(head)
            continue
        elif kind == "random":
            n = cur.take_int()
            if n == 0:
                args.append(None)
                continue
            vals, rands = [], []
            for _ in range(n):
                line = cur.take_line().split()
                vals.append(int(line[0]))
                rands.append(int(line[1]))
            nodes = [Node(v) for v in vals]
            for j in range(n):
                if j + 1 < n:
                    nodes[j].next = nodes[j + 1]
                if rands[j] != -1:
                    nodes[j].random = nodes[rands[j]]
            args.append(nodes[0])
            continue
        elif kind == "intersect":
            n_a = cur.take_int()
            va = [cur.take_int() for _ in range(n_a)] if n_a else []
            n_b = cur.take_int()
            vb = [cur.take_int() for _ in range(n_b)] if n_b else []
            skip_a = cur.take_int()
            skip_b = cur.take_int()
            head_a, nodes_a = _build_list(va)
            if skip_a < 0:
                head_b, _ = _build_list(vb)
            else:
                dummy = ListNode()
                t = dummy
                for j in range(skip_b):
                    t.next = ListNode(vb[j])
                    t = t.next
                t.next = nodes_a[skip_a]
                head_b = dummy.next
            args.extend([head_a, head_b])
            continue
        elif kind == "lca":
            root = cur.take_tree()
            p, q = cur.take_int(), cur.take_int()
            args.extend([root, _find_node(root, p), _find_node(root, q)])
            continue
        else:
            raise ValueError(kind)
        if first_mut is None:
            first_mut = val
        args.append(val)
    sol = Solution()
    result = getattr(sol, SPEC["method"])(*args)
    _print_ret(SPEC["returns"], result, first_mut, args)


def _run_design():
    cur = _Cur()
    q = cur.take_int()
    cls = globals()[SPEC["class"]]
    obj = None
    for _ in range(q):
        parts = cur.take_line().split()
        op = parts[0]
        if op == SPEC["class"]:
            ctor = SPEC.get("ctor") or []
            argv = []
            for t, raw in zip(ctor, parts[1:], strict=False):
                argv.append(int(raw) if t == "int" else raw)
            obj = cls(*argv)
            print("null")
            continue
        meta = SPEC["methods"][op]
        argv = []
        for t, raw in zip(meta["params"], parts[1:], strict=False):
            argv.append(int(raw) if t == "int" else raw)
        ret = getattr(obj, op)(*argv)
        rk = meta["returns"]
        if rk == "void":
            print("null")
        elif rk == "bool":
            print("true" if ret else "false")
        elif rk == "float":
            print(f"{float(ret):.1f}")
        else:
            print(ret)


if __name__ == "__main__":
    if SPEC["kind"] == "design":
        _run_design()
    else:
        _run_fn()
'''


def wrap_python(user_code: str, spec: dict[str, Any]) -> str:
    payload = json.dumps(json.dumps(spec, ensure_ascii=False))
    runtime = _PY_RUNTIME.replace("__SPEC__", payload)
    return _PY_PREAMBLE + _strip_user_main(user_code) + "\n" + runtime.lstrip("\n")


_CPP_PREAMBLE = r"""
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Node {
public:
    int val;
    Node* next;
    Node* random;
    Node(int _val) : val(_val), next(nullptr), random(nullptr) {}
};

static vector<string> LINES;
static int LI = 0;
static vector<string> BUF;

void init_io() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    while (getline(cin, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        LINES.push_back(line);
    }
}

void fill_tok() {
    while (BUF.empty() && LI < (int)LINES.size()) {
        stringstream ss(LINES[LI++]);
        string t;
        while (ss >> t) BUF.push_back(t);
    }
}

int take_int() {
    fill_tok();
    int v = stoi(BUF.front());
    BUF.erase(BUF.begin());
    return v;
}

string take_tok() {
    fill_tok();
    string v = BUF.front();
    BUF.erase(BUF.begin());
    return v;
}

string take_line() {
    if (!BUF.empty()) {
        string s;
        for (size_t i = 0; i < BUF.size(); i++) {
            if (i) s += ' ';
            s += BUF[i];
        }
        BUF.clear();
        return s;
    }
    if (LI < (int)LINES.size()) return LINES[LI++];
    return "";
}

vector<int> take_vec() {
    int n = take_int();
    vector<int> a(n);
    for (int i = 0; i < n; i++) a[i] = take_int();
    return a;
}

vector<vector<int>> take_vec2() {
    int m = take_int(), n = take_int();
    vector<vector<int>> g(m, vector<int>(n));
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) g[i][j] = take_int();
    return g;
}

vector<vector<char>> take_board() {
    int m = take_int(), n = take_int();
    vector<vector<char>> g(m, vector<char>(n));
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        string t = take_tok();
        g[i][j] = t.empty() ? ' ' : t[0];
    }
    return g;
}

vector<vector<char>> take_grid01() {
    int m = take_int(), n = take_int();
    vector<vector<char>> g(m, vector<char>(n));
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        int x = take_int();
        g[i][j] = x == 1 ? '1' : '0';
    }
    return g;
}

vector<vector<int>> take_intervals() {
    int m = take_int(), n = take_int();
    vector<vector<int>> a;
    for (int i = 0; i < m; i++) {
        int x = take_int(), y = take_int();
        a.push_back({x, y});
        for (int k = 2; k < n; k++) take_int();
    }
    return a;
}

pair<ListNode*, vector<ListNode*>> build_list(const vector<int>& vals) {
    ListNode dummy;
    ListNode* t = &dummy;
    vector<ListNode*> nodes;
    for (int v : vals) {
        t->next = new ListNode(v);
        t = t->next;
        nodes.push_back(t);
    }
    return {dummy.next, nodes};
}

ListNode* take_list() {
    int n = take_int();
    vector<int> vals(n);
    for (int i = 0; i < n; i++) vals[i] = take_int();
    return build_list(vals).first;
}

TreeNode* build_tree(const vector<string>& tokens) {
    int n = (int)tokens.size();
    if (n == 0) return nullptr;
    auto parse = [&](int i) -> TreeNode* {
        if (tokens[i] == "null") return nullptr;
        return new TreeNode(stoi(tokens[i]));
    };
    TreeNode* root = parse(0);
    queue<TreeNode*> q;
    if (root) q.push(root);
    int i = 1;
    while (!q.empty() && i < n) {
        TreeNode* node = q.front(); q.pop();
        if (i < n) {
            node->left = parse(i);
            if (node->left) q.push(node->left);
            i++;
        }
        if (i < n) {
            node->right = parse(i);
            if (node->right) q.push(node->right);
            i++;
        }
    }
    return root;
}

TreeNode* take_tree() {
    int n = take_int();
    vector<string> tokens;
    for (int i = 0; i < n; i++) tokens.push_back(take_tok());
    return build_tree(tokens);
}

TreeNode* find_node(TreeNode* root, int val) {
    if (!root) return nullptr;
    if (root->val == val) return root;
    TreeNode* L = find_node(root->left, val);
    return L ? L : find_node(root->right, val);
}

void print_vec(const vector<int>& a) {
    for (size_t i = 0; i < a.size(); i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
}

void print_list(ListNode* head) {
    vector<int> vals;
    while (head) { vals.push_back(head->val); head = head->next; }
    if (vals.empty()) { cout << 0 << '\n'; return; }
    cout << vals.size() << '\n';
    print_vec(vals);
}

void print_tree(TreeNode* root) {
    if (!root) { cout << 0 << '\n'; return; }
    queue<TreeNode*> q;
    q.push(root);
    vector<string> tokens;
    while (!q.empty()) {
        TreeNode* node = q.front(); q.pop();
        if (!node) { tokens.push_back("null"); continue; }
        tokens.push_back(to_string(node->val));
        q.push(node->left);
        q.push(node->right);
    }
    while (!tokens.empty() && tokens.back() == "null") tokens.pop_back();
    cout << tokens.size() << '\n';
    for (size_t i = 0; i < tokens.size(); i++) {
        if (i) cout << ' ';
        cout << tokens[i];
    }
    cout << '\n';
}

void print_int_rows(vector<vector<int>> rows, const string& mode) {
    if (mode != "perms") {
        for (auto& r : rows) sort(r.begin(), r.end());
    }
    if (mode == "subsets") {
        sort(rows.begin(), rows.end(), [](const vector<int>& a, const vector<int>& b) {
            if (a.size() != b.size()) return a.size() < b.size();
            return a < b;
        });
    } else {
        sort(rows.begin(), rows.end());
    }
    for (auto& r : rows) print_vec(r);
}

"""


def wrap_cpp(user_code: str, spec: dict[str, Any]) -> str:
    return _CPP_PREAMBLE + "\n" + user_code.rstrip() + "\n\n" + _cpp_driver(spec) + "\n"


def _cpp_driver(spec: dict[str, Any]) -> str:
    if spec["kind"] == "design":
        return _cpp_design_driver(spec)
    return _cpp_fn_driver(spec)


def _cpp_design_driver(spec: dict[str, Any]) -> str:
    cls = spec["class"]
    methods = spec["methods"]
    lines = [
        "int main() {",
        "    init_io();",
        f"    {cls}* obj = nullptr;",
        "    int q = take_int();",
        "    for (int i = 0; i < q; i++) {",
        "        string line = take_line();",
        "        stringstream ss(line);",
        "        string op; ss >> op;",
        f'        if (op == "{cls}") {{',
    ]
    ctor = spec.get("ctor") or []
    if ctor == ["int"]:
        lines.append("            int a; ss >> a;")
        lines.append(f"            obj = new {cls}(a);")
    else:
        lines.append(f"            obj = new {cls}();")
    lines.append('            cout << "null\\n";')
    lines.append("            continue;")
    lines.append("        }")
    for name, meta in methods.items():
        lines.append(f'        if (op == "{name}") {{')
        params = list(meta["params"])
        decls: list[str] = []
        for j, t in enumerate(params):
            v = f"v{j}"
            if t == "int":
                lines.append(f"            int {v}; ss >> {v};")
            else:
                lines.append(f"            string {v}; ss >> {v};")
            decls.append(v)
        call = ", ".join(decls)
        ret = str(meta["returns"])
        if ret == "void":
            lines.append(f"            obj->{name}({call});")
            lines.append('            cout << "null\\n";')
        elif ret == "bool":
            lines.append(
                f'            cout << (obj->{name}({call}) ? "true" : "false") << "\\n";'
            )
        elif ret == "float":
            lines.append("            cout << fixed << setprecision(1);")
            lines.append(f"            cout << obj->{name}({call}) << \"\\n\";")
        else:
            lines.append(f"            cout << obj->{name}({call}) << \"\\n\";")
        lines.append("            continue;")
        lines.append("        }")
    lines.append("    }")
    lines.append("    return 0;")
    lines.append("}")
    return "\n".join(lines)


def _cpp_fn_driver(spec: dict[str, Any]) -> str:
    method = spec["method"]
    params = spec["params"]
    ret = spec["returns"]
    names = list(spec.get("names") or [])
    body = [
        "int main() {",
        "    init_io();",
        "    Solution sol;",
    ]
    call_args: list[str] = []
    first = names[0] if names else "arg0"

    def add_lines(xs: list[str]) -> None:
        body.extend(xs)

    for idx, kind in enumerate(params):
        var = names[idx] if idx < len(names) else f"arg{idx}"
        if kind == "int":
            add_lines([f"    int {var} = take_int();"])
            call_args.append(var)
        elif kind == "vec":
            add_lines([f"    vector<int> {var} = take_vec();"])
            call_args.append(var)
        elif kind == "vec2":
            add_lines([f"    vector<vector<int>> {var} = take_vec2();"])
            call_args.append(var)
        elif kind == "intervals":
            add_lines([f"    vector<vector<int>> {var} = take_intervals();"])
            call_args.append(var)
        elif kind == "str":
            add_lines([f"    string {var} = take_line();"])
            call_args.append(var)
        elif kind == "strs":
            add_lines(
                [
                    f"    int {var}_n = take_int();",
                    f"    vector<string> {var}({var}_n);",
                    f"    for (int i = 0; i < {var}_n; i++) {var}[i] = take_line();",
                ]
            )
            call_args.append(var)
        elif kind == "listnode":
            add_lines([f"    ListNode* {var} = take_list();"])
            call_args.append(var)
        elif kind == "listnodes":
            add_lines(
                [
                    "    int k = take_int();",
                    "    vector<ListNode*> lists(k);",
                    "    for (int i = 0; i < k; i++) lists[i] = take_list();",
                ]
            )
            call_args.append("lists")
        elif kind == "tree":
            add_lines([f"    TreeNode* {var} = take_tree();"])
            call_args.append(var)
        elif kind == "grid01":
            add_lines([f"    vector<vector<char>> {var} = take_grid01();"])
            call_args.append(var)
        elif kind == "board":
            add_lines([f"    vector<vector<char>> {var} = take_board();"])
            call_args.append(var)
        elif kind == "edges":
            add_lines(
                [
                    "    int numCourses = take_int();",
                    "    int m = take_int();",
                    "    take_int();",
                    "    vector<vector<int>> prerequisites;",
                    "    for (int i = 0; i < m; i++) {",
                    "        int a = take_int(), b = take_int();",
                    "        prerequisites.push_back({a, b});",
                    "    }",
                ]
            )
            call_args.extend(["numCourses", "prerequisites"])
        elif kind == "cycle":
            add_lines(
                [
                    "    int n = take_int();",
                    "    ListNode* head = nullptr;",
                    "    if (n > 0) {",
                    "        vector<int> vals(n);",
                    "        for (int i = 0; i < n; i++) vals[i] = take_int();",
                    "        int pos = take_int();",
                    "        auto built = build_list(vals);",
                    "        head = built.first;",
                    "        if (pos >= 0 && pos < n) built.second.back()->next = built.second[pos];",
                    "    }",
                ]
            )
            call_args.append("head")
        elif kind == "random":
            add_lines(
                [
                    "    int n = take_int();",
                    "    Node* head = nullptr;",
                    "    if (n > 0) {",
                    "        vector<int> vals(n), rands(n);",
                    "        for (int i = 0; i < n; i++) {",
                    "            stringstream ss(take_line());",
                    "            ss >> vals[i] >> rands[i];",
                    "        }",
                    "        vector<Node*> nodes;",
                    "        for (int v : vals) nodes.push_back(new Node(v));",
                    "        for (int i = 0; i < n; i++) {",
                    "            if (i + 1 < n) nodes[i]->next = nodes[i + 1];",
                    "            if (rands[i] != -1) nodes[i]->random = nodes[rands[i]];",
                    "        }",
                    "        head = nodes[0];",
                    "    }",
                ]
            )
            call_args.append("head")
        elif kind == "intersect":
            add_lines(
                [
                    "    int na = take_int();",
                    "    vector<int> va(na);",
                    "    for (int i = 0; i < na; i++) va[i] = take_int();",
                    "    int nb = take_int();",
                    "    vector<int> vb(nb);",
                    "    for (int i = 0; i < nb; i++) vb[i] = take_int();",
                    "    int skip_a = take_int(), skip_b = take_int();",
                    "    auto built_a = build_list(va);",
                    "    ListNode* headA = built_a.first;",
                    "    ListNode* headB = nullptr;",
                    "    if (skip_a < 0) headB = build_list(vb).first;",
                    "    else {",
                    "        ListNode dummy; ListNode* t = &dummy;",
                    "        for (int j = 0; j < skip_b; j++) { t->next = new ListNode(vb[j]); t = t->next; }",
                    "        t->next = built_a.second[skip_a];",
                    "        headB = dummy.next;",
                    "    }",
                ]
            )
            call_args.extend(["headA", "headB"])
        elif kind == "lca":
            add_lines(
                [
                    "    TreeNode* root = take_tree();",
                    "    int pv = take_int(), qv = take_int();",
                    "    TreeNode* p = find_node(root, pv);",
                    "    TreeNode* q = find_node(root, qv);",
                ]
            )
            call_args.extend(["root", "p", "q"])
        else:
            add_lines([f"    int {var} = take_int();"])
            call_args.append(var)

    args = ", ".join(call_args)
    call = f"sol.{method}({args})"
    if ret == "void_vec":
        add_lines([f"    {call};", f"    print_vec({first});"])
    elif ret == "void_mat":
        add_lines(
            [
                f"    {call};",
                f"    cout << {first}.size() << ' ' << ({first}.empty() ? 0 : {first}[0].size()) << '\\n';",
                f"    for (auto& row : {first}) print_vec(row);",
            ]
        )
    elif ret == "void_tree":
        add_lines([f"    {call};", f"    print_tree({first});"])
    elif ret == "int":
        add_lines([f"    cout << {call} << '\\n';"])
    elif ret == "bool":
        add_lines([f'    cout << ({call} ? "true" : "false") << "\\n";'])
    elif ret == "float":
        add_lines(["    cout << fixed << setprecision(1);", f"    cout << {call} << '\\n';"])
    elif ret == "str":
        add_lines([f"    cout << {call} << '\\n';"])
    elif ret == "vec":
        add_lines([f"    vector<int> ans = {call};"])
        if spec.get("sort"):
            add_lines(["    sort(ans.begin(), ans.end());"])
        elif spec.get("rank") == "freq":
            add_lines(
                [
                    "    unordered_map<int,int> cnt;",
                    f"    for (int x : {first}) cnt[x]++;",
                    "    sort(ans.begin(), ans.end(), [&](int a, int b) {",
                    "        if (cnt[a] != cnt[b]) return cnt[a] > cnt[b];",
                    "        return a < b;",
                    "    });",
                ]
            )
        add_lines(["    print_vec(ans);"])
    elif ret == "listnode":
        add_lines([f"    print_list({call});"])
    elif ret == "tree":
        add_lines([f"    print_tree({call});"])
    elif ret in ("lines", "perms", "subsets"):
        add_lines([f'    print_int_rows({call}, "{ret}");'])
    elif ret == "str_lines":
        add_lines(
            [
                f"    vector<string> ans = {call};",
                "    sort(ans.begin(), ans.end());",
                "    for (auto& s : ans) cout << s << '\\n';",
            ]
        )
    elif ret == "str_lines_space":
        add_lines(
            [
                f"    vector<vector<string>> ans = {call};",
                "    for (auto& r : ans) sort(r.begin(), r.end());",
                "    sort(ans.begin(), ans.end());",
                "    for (auto& r : ans) {",
                "        for (size_t i = 0; i < r.size(); i++) { if (i) cout << ' '; cout << r[i]; }",
                "        cout << '\\n';",
                "    }",
            ]
        )
    elif ret == "groups":
        add_lines(
            [
                f"    vector<vector<string>> ans = {call};",
                "    for (auto& r : ans) sort(r.begin(), r.end());",
                "    sort(ans.begin(), ans.end(), [](const vector<string>& a, const vector<string>& b) {",
                '        string aa = a.empty() ? "" : a[0];',
                '        string bb = b.empty() ? "" : b[0];',
                "        return aa < bb;",
                "    });",
                "    for (auto& r : ans) {",
                "        for (size_t i = 0; i < r.size(); i++) { if (i) cout << ' '; cout << r[i]; }",
                "        cout << '\\n';",
                "    }",
            ]
        )
    elif ret == "nqueens":
        add_lines([f"    cout << {call}.size() << '\\n';"])
    elif ret == "pascal":
        add_lines(
            [
                f"    vector<vector<int>> ans = {call};",
                "    for (auto& row : ans) print_vec(row);",
            ]
        )
    elif ret == "levels":
        add_lines(
            [
                f"    vector<vector<int>> ans = {call};",
                "    for (auto& row : ans) print_vec(row);",
            ]
        )
    elif ret == "intervals":
        add_lines(
            [
                f"    vector<vector<int>> ans = {call};",
                "    for (auto& it : ans) cout << it[0] << ' ' << it[1] << '\\n';",
            ]
        )
    elif ret == "cycle_val":
        add_lines(
            [
                f"    ListNode* ans = {call};",
                "    cout << (ans ? ans->val : -1) << '\\n';",
            ]
        )
    elif ret == "lca_val":
        add_lines([f"    cout << {call}->val << '\\n';"])
    elif ret == "random":
        add_lines(
            [
                f"    Node* ans = {call};",
                "    if (!ans) { cout << 0 << '\\n'; return 0; }",
                "    vector<Node*> arr;",
                "    for (Node* c = ans; c; c = c->next) arr.push_back(c);",
                "    unordered_map<Node*, int> idx;",
                "    for (int i = 0; i < (int)arr.size(); i++) idx[arr[i]] = i;",
                "    cout << arr.size() << '\\n';",
                "    for (Node* node : arr) {",
                "        int ri = node->random ? idx[node->random] : -1;",
                "        cout << node->val << ' ' << ri << '\\n';",
                "    }",
            ]
        )
    else:
        add_lines([f"    {call};"])
    add_lines(["    return 0;", "}"])
    return "\n".join(body)


def wrap_user_code(language: str, user_code: str, spec: dict[str, Any] | None) -> str:
    if not spec:
        raise ValueError("本题暂不支持力扣函数模式，请切换到 ACM 模式")
    if language == "python3":
        return wrap_python(user_code, spec)
    if language == "cpp":
        return wrap_cpp(user_code, spec)
    raise ValueError(f"不支持的语言: {language}")
