import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n").rstrip("\r")
    n = len(s)
    ans: list[str] = []
    path: list[str] = []

    def is_pal(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    def dfs(start: int) -> None:
        if start == n:
            ans.append(" ".join(path))
            return
        for end in range(start, n):
            if is_pal(start, end):
                path.append(s[start : end + 1])
                dfs(end + 1)
                path.pop()

    dfs(0)
    ans.sort()
    sys.stdout.write("\n".join(ans))
    if ans:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
