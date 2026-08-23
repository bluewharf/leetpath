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
    data = sys.stdin.read().split()
    n = int(data[0])
    h = list(map(int, data[1 : 1 + n]))
    print(largest_rectangle(h))


if __name__ == "__main__":
    main()
