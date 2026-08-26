"""每题力扣函数签名。评测仍用 ACM 用例，由 wrap 负责读入并调用 Solution。"""

from __future__ import annotations

from typing import Any

Spec = dict[str, Any]


def fn(
    method: str,
    params: list[str],
    ret: str,
    names: list[str] | None = None,
    **extra: object,
) -> Spec:
    spec: Spec = {
        "kind": "fn",
        "class": "Solution",
        "method": method,
        "params": params,
        "returns": ret,
    }
    if names:
        spec["names"] = names
    spec.update(extra)
    return spec


def design(cls: str, ctor: list[str], methods: dict[str, dict[str, object]]) -> Spec:
    return {"kind": "design", "class": cls, "ctor": ctor, "methods": methods}


# params: int, vec, vec2, intervals, str, strs, listnode, listnodes, tree,
#         edges, cycle, random, intersect, grid01, board, lca
# returns: int, float, bool, str, vec, listnode, tree, lines, perms, subsets,
#          str_lines, str_lines_space, groups, intervals, void_vec, void_mat,
#          void_tree, nqueens, pascal, random, cycle_val, lca_val, levels

SPECS: dict[str, Spec] = {
    "two-sum": fn("twoSum", ["vec", "int"], "vec", ["nums", "target"], sort=True),
    "add-two-numbers": fn("addTwoNumbers", ["listnode", "listnode"], "listnode", ["l1", "l2"]),
    "longest-substring-without-repeating-characters": fn(
        "lengthOfLongestSubstring", ["str"], "int", ["s"]
    ),
    "median-of-two-sorted-arrays": fn(
        "findMedianSortedArrays", ["vec", "vec"], "float", ["nums1", "nums2"]
    ),
    "longest-palindromic-substring": fn("longestPalindrome", ["str"], "str", ["s"]),
    "3sum": fn("threeSum", ["vec"], "lines", ["nums"]),
    "letter-combinations-of-a-phone-number": fn(
        "letterCombinations", ["str"], "str_lines", ["digits"]
    ),
    "generate-parentheses": fn("generateParenthesis", ["int"], "str_lines", ["n"]),
    "merge-k-sorted-lists": fn("mergeKLists", ["listnodes"], "listnode", ["lists"]),
    "next-permutation": fn("nextPermutation", ["vec"], "void_vec", ["nums"]),
    "search-in-rotated-sorted-array": fn("search", ["vec", "int"], "int", ["nums", "target"]),
    "find-first-and-last-position-of-element-in-sorted-array": fn(
        "searchRange", ["vec", "int"], "vec", ["nums", "target"]
    ),
    "search-insert-position": fn("searchInsert", ["vec", "int"], "int", ["nums", "target"]),
    "valid-parentheses": fn("isValid", ["str"], "bool", ["s"]),
    "merge-two-sorted-lists": fn(
        "mergeTwoLists", ["listnode", "listnode"], "listnode", ["l1", "l2"]
    ),
    "swap-nodes-in-pairs": fn("swapPairs", ["listnode"], "listnode", ["head"]),
    "reverse-nodes-in-k-group": fn("reverseKGroup", ["listnode", "int"], "listnode", ["head", "k"]),
    "remove-nth-node-from-end-of-list": fn(
        "removeNthFromEnd", ["listnode", "int"], "listnode", ["head", "n"]
    ),
    "longest-valid-parentheses": fn("longestValidParentheses", ["str"], "int", ["s"]),
    "container-with-most-water": fn("maxArea", ["vec"], "int", ["height"]),
    "trapping-rain-water": fn("trap", ["vec"], "int", ["height"]),
    "combination-sum": fn("combinationSum", ["vec", "int"], "lines", ["candidates", "target"]),
    "permutations": fn("permute", ["vec"], "perms", ["nums"]),
    "rotate-image": fn("rotate", ["vec2"], "void_mat", ["matrix"]),
    "group-anagrams": fn("groupAnagrams", ["strs"], "groups", ["strs"]),
    "maximum-subarray": fn("maxSubArray", ["vec"], "int", ["nums"]),
    "spiral-matrix": fn("spiralOrder", ["vec2"], "vec", ["matrix"]),
    "jump-game": fn("canJump", ["vec"], "bool", ["nums"]),
    "merge-intervals": fn("merge", ["intervals"], "intervals", ["intervals"]),
    "unique-paths": fn("uniquePaths", ["int", "int"], "int", ["m", "n"]),
    "minimum-path-sum": fn("minPathSum", ["vec2"], "int", ["grid"]),
    "climbing-stairs": fn("climbStairs", ["int"], "int", ["n"]),
    "edit-distance": fn("minDistance", ["str", "str"], "int", ["word1", "word2"]),
    "set-matrix-zeroes": fn("setZeroes", ["vec2"], "void_mat", ["matrix"]),
    "search-a-2d-matrix": fn("searchMatrix", ["vec2", "int"], "bool", ["matrix", "target"]),
    "sort-colors": fn("sortColors", ["vec"], "void_vec", ["nums"]),
    "minimum-window-substring": fn("minWindow", ["str", "str"], "str", ["s", "t"]),
    "subsets": fn("subsets", ["vec"], "subsets", ["nums"]),
    "word-search": fn("exist", ["board", "str"], "bool", ["board", "word"]),
    "largest-rectangle-in-histogram": fn("largestRectangleArea", ["vec"], "int", ["heights"]),
    "binary-tree-inorder-traversal": fn("inorderTraversal", ["tree"], "vec", ["root"]),
    "validate-binary-search-tree": fn("isValidBST", ["tree"], "bool", ["root"]),
    "symmetric-tree": fn("isSymmetric", ["tree"], "bool", ["root"]),
    "binary-tree-level-order-traversal": fn("levelOrder", ["tree"], "levels", ["root"]),
    "maximum-depth-of-binary-tree": fn("maxDepth", ["tree"], "int", ["root"]),
    "construct-binary-tree-from-preorder-and-inorder-traversal": fn(
        "buildTree", ["vec", "vec"], "tree", ["preorder", "inorder"]
    ),
    "flatten-binary-tree-to-linked-list": fn("flatten", ["tree"], "void_tree", ["root"]),
    "best-time-to-buy-and-sell-stock": fn("maxProfit", ["vec"], "int", ["prices"]),
    "binary-tree-maximum-path-sum": fn("maxPathSum", ["tree"], "int", ["root"]),
    "longest-consecutive-sequence": fn("longestConsecutive", ["vec"], "int", ["nums"]),
    "single-number": fn("singleNumber", ["vec"], "int", ["nums"]),
    "word-break": fn("wordBreak", ["str", "strs"], "bool", ["s", "wordDict"]),
    "linked-list-cycle": fn("hasCycle", ["cycle"], "bool", ["head"]),
    "linked-list-cycle-ii": fn("detectCycle", ["cycle"], "cycle_val", ["head"]),
    "copy-list-with-random-pointer": fn("copyRandomList", ["random"], "random", ["head"]),
    "sort-list": fn("sortList", ["listnode"], "listnode", ["head"]),
    "intersection-of-two-linked-lists": fn(
        "getIntersectionNode", ["intersect"], "cycle_val", ["headA", "headB"]
    ),
    "majority-element": fn("majorityElement", ["vec"], "int", ["nums"]),
    "rotate-array": fn("rotate", ["vec", "int"], "void_vec", ["nums", "k"]),
    "reverse-linked-list": fn("reverseList", ["listnode"], "listnode", ["head"]),
    "house-robber": fn("rob", ["vec"], "int", ["nums"]),
    "number-of-islands": fn("numIslands", ["grid01"], "int", ["grid"]),
    "kth-smallest-element-in-a-bst": fn("kthSmallest", ["tree", "int"], "int", ["root", "k"]),
    "lowest-common-ancestor-of-a-binary-tree": fn(
        "lowestCommonAncestor", ["lca"], "lca_val", ["root", "p", "q"]
    ),
    "product-of-array-except-self": fn("productExceptSelf", ["vec"], "vec", ["nums"]),
    "sliding-window-maximum": fn("maxSlidingWindow", ["vec", "int"], "vec", ["nums", "k"]),
    "search-a-2d-matrix-ii": fn("searchMatrix", ["vec2", "int"], "bool", ["matrix", "target"]),
    "coin-change": fn("coinChange", ["vec", "int"], "int", ["coins", "amount"]),
    "longest-increasing-subsequence": fn("lengthOfLIS", ["vec"], "int", ["nums"]),
    "min-stack": design(
        "MinStack",
        [],
        {
            "push": {"params": ["int"], "returns": "void"},
            "pop": {"params": [], "returns": "void"},
            "top": {"params": [], "returns": "int"},
            "getMin": {"params": [], "returns": "int"},
        },
    ),
    "decode-string": fn("decodeString", ["str"], "str", ["s"]),
    "perfect-squares": fn("numSquares", ["int"], "int", ["n"]),
    "move-zeroes": fn("moveZeroes", ["vec"], "void_vec", ["nums"]),
    "find-the-duplicate-number": fn("findDuplicate", ["vec"], "int", ["nums"]),
    "find-all-anagrams-in-a-string": fn("findAnagrams", ["str", "str"], "vec", ["s", "p"]),
    "first-missing-positive": fn("firstMissingPositive", ["vec"], "int", ["nums"]),
    "find-median-from-data-stream": design(
        "MedianFinder",
        [],
        {
            "addNum": {"params": ["int"], "returns": "void"},
            "findMedian": {"params": [], "returns": "float"},
        },
    ),
    "path-sum-iii": fn("pathSum", ["tree", "int"], "int", ["root", "targetSum"]),
    "diameter-of-binary-tree": fn("diameterOfBinaryTree", ["tree"], "int", ["root"]),
    "subarray-sum-equals-k": fn("subarraySum", ["vec", "int"], "int", ["nums", "k"]),
    "daily-temperatures": fn("dailyTemperatures", ["vec"], "vec", ["temperatures"]),
    "longest-common-subsequence": fn(
        "longestCommonSubsequence", ["str", "str"], "int", ["text1", "text2"]
    ),
    "n-queens": fn("solveNQueens", ["int"], "nqueens", ["n"]),
    "implement-trie-prefix-tree": design(
        "Trie",
        [],
        {
            "insert": {"params": ["str"], "returns": "void"},
            "search": {"params": ["str"], "returns": "bool"},
            "startsWith": {"params": ["str"], "returns": "bool"},
        },
    ),
    "lru-cache": design(
        "LRUCache",
        ["int"],
        {
            "get": {"params": ["int"], "returns": "int"},
            "put": {"params": ["int", "int"], "returns": "void"},
        },
    ),
    "find-minimum-in-rotated-sorted-array": fn("findMin", ["vec"], "int", ["nums"]),
    "kth-largest-element-in-an-array": fn("findKthLargest", ["vec", "int"], "int", ["nums", "k"]),
    "invert-binary-tree": fn("invertTree", ["tree"], "tree", ["root"]),
    "palindrome-linked-list": fn("isPalindrome", ["listnode"], "bool", ["head"]),
    "jump-game-ii": fn("jump", ["vec"], "int", ["nums"]),
    "maximum-product-subarray": fn("maxProduct", ["vec"], "int", ["nums"]),
    "binary-tree-right-side-view": fn("rightSideView", ["tree"], "vec", ["root"]),
    "course-schedule": fn("canFinish", ["edges"], "bool", ["numCourses", "prerequisites"]),
    "convert-sorted-array-to-binary-search-tree": fn(
        "sortedArrayToBST", ["vec"], "tree", ["nums"]
    ),
    "palindrome-partitioning": fn("partition", ["str"], "str_lines_space", ["s"]),
    "partition-equal-subset-sum": fn("canPartition", ["vec"], "bool", ["nums"]),
    "partition-labels": fn("partitionLabels", ["str"], "vec", ["s"]),
    "pascals-triangle": fn("generate", ["int"], "pascal", ["numRows"]),
    "rotting-oranges": fn("orangesRotting", ["vec2"], "int", ["grid"]),
    "top-k-frequent-elements": fn(
        "topKFrequent", ["vec", "int"], "vec", ["nums", "k"], rank="freq"
    ),
}


def spec_for(slug: str) -> dict | None:
    return SPECS.get(slug)


def spec_for_problem(problem: object) -> dict | None:
    spec = getattr(problem, "leetcode_spec", None)
    if isinstance(spec, dict) and spec.get("kind"):
        return spec
    return spec_for(str(getattr(problem, "slug", "") or ""))
