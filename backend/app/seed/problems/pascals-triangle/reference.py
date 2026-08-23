import sys


def main() -> None:
    n = int(sys.stdin.read().strip())
    triangle: list[list[int]] = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
        print(" ".join(str(x) for x in row))


if __name__ == "__main__":
    main()
