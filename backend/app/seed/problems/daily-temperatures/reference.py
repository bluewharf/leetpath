import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    temps = data[1 : 1 + n]
    ans = [0] * n
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
