import sys
from collections import defaultdict


def main() -> None:
    data = sys.stdin.read()
    lines = data.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    n = int(lines[0])
    strs = lines[1 : 1 + n]
    while len(strs) < n:
        strs.append("")
    groups: dict[str, list[str]] = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    result = []
    for g in groups.values():
        g.sort()
        result.append(g)
    result.sort(key=lambda g: g[0])
    for g in result:
        print(" ".join(g))


if __name__ == "__main__":
    main()
