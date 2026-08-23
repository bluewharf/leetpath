import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    candidates = list(map(int, data[1 : 1 + n]))
    target = int(data[1 + n])
    candidates.sort()
    res: list[list[int]] = []

    def dfs(start: int, remain: int, path: list[int]) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, n):
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            dfs(i, remain - c, path)
            path.pop()

    dfs(0, target, [])
    res.sort()
    for comb in res:
        print(" ".join(map(str, comb)))


if __name__ == "__main__":
    main()
