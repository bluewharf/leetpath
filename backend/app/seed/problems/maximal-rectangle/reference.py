import sys


def largest_rectangle(heights: list[int]) -> int:
    heights = heights + [0]
    stack = [-1]
    ans = 0
    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            area = height * width
            if area > ans:
                ans = area
        stack.append(i)
    return ans


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    height = [0] * n
    ans = 0
    for i in range(m):
        for j in range(n):
            height[j] = height[j] + 1 if mat[i][j] == 1 else 0
        area = largest_rectangle(height)
        if area > ans:
            ans = area
    print(ans)


if __name__ == "__main__":
    main()
