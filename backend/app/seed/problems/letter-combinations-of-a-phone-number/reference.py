import sys

MAPPING = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def main() -> None:
    digits = sys.stdin.readline().rstrip("\n")
    if not digits:
        return
    ans: list[str] = []

    def dfs(i: int, path: list[str]) -> None:
        if i == len(digits):
            ans.append("".join(path))
            return
        for ch in MAPPING[digits[i]]:
            path.append(ch)
            dfs(i + 1, path)
            path.pop()

    dfs(0, [])
    ans.sort()
    for s in ans:
        print(s)


if __name__ == "__main__":
    main()
