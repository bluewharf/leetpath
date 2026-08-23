import sys


def main() -> None:
    s = sys.stdin.readline()
    if s.endswith("\n"):
        s = s[:-1]
    last = {c: i for i, c in enumerate(s)}
    start = 0
    end = 0
    parts: list[int] = []
    for i, c in enumerate(s):
        if last[c] > end:
            end = last[c]
        if i == end:
            parts.append(i - start + 1)
            start = i + 1
    print(" ".join(map(str, parts)))


if __name__ == "__main__":
    main()
