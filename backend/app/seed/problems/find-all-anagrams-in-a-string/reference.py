import sys


def main() -> None:
    lines = sys.stdin.read().splitlines()
    s = lines[0] if len(lines) > 0 else ""
    p = lines[1] if len(lines) > 1 else ""
    ns, np = len(s), len(p)
    if np == 0 or ns < np:
        print()
        return
    need = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    win = [0] * 26
    for i in range(np):
        win[ord(s[i]) - 97] += 1
    ans: list[int] = []
    if win == need:
        ans.append(0)
    for i in range(np, ns):
        win[ord(s[i]) - 97] += 1
        win[ord(s[i - np]) - 97] -= 1
        if win == need:
            ans.append(i - np + 1)
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    main()
