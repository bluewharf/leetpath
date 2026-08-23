import sys


def exist(board: list[list[str]], word: str) -> bool:
    m, n = len(board), len(board[0])
    wlen = len(word)
    if wlen > m * n:
        return False

    def dfs(i: int, j: int, k: int) -> bool:
        if k == wlen:
            return True
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        tmp = board[i][j]
        board[i][j] = "#"
        found = (
            dfs(i + 1, j, k + 1)
            or dfs(i - 1, j, k + 1)
            or dfs(i, j + 1, k + 1)
            or dfs(i, j - 1, k + 1)
        )
        board[i][j] = tmp
        return found

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True
    return False


def main() -> None:
    data = sys.stdin.read().split()
    m, n = int(data[0]), int(data[1])
    idx = 2
    board: list[list[str]] = []
    for _ in range(m):
        board.append(list(data[idx : idx + n]))
        idx += n
    word = data[idx]
    print("true" if exist(board, word) else "false")


if __name__ == "__main__":
    main()
