import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    m, n = data[0], data[1]
    mat = []
    idx = 2
    for _ in range(m):
        mat.append(data[idx : idx + n])
        idx += n
    ans: list[int] = []
    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            ans.append(mat[top][j])
        top += 1
        for i in range(top, bottom + 1):
            ans.append(mat[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                ans.append(mat[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                ans.append(mat[i][left])
            left += 1
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
