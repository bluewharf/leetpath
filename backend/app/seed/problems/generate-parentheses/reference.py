import sys


def main() -> None:
    n = int(sys.stdin.read().strip())
    ans: list[str] = []

    def dfs(cur: list[str], open_cnt: int, close_cnt: int) -> None:
        if len(cur) == 2 * n:
            ans.append("".join(cur))
            return
        if open_cnt < n:
            cur.append("(")
            dfs(cur, open_cnt + 1, close_cnt)
            cur.pop()
        if close_cnt < open_cnt:
            cur.append(")")
            dfs(cur, open_cnt, close_cnt + 1)
            cur.pop()

    dfs([], 0, 0)
    ans.sort()
    for s in ans:
        print(s)


if __name__ == "__main__":
    main()
