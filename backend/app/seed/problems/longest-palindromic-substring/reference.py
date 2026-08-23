import sys

def expand(s, l, r):
    n = len(s)
    while l >= 0 and r < n and s[l] == s[r]:
        l -= 1
        r += 1
    return s[l + 1 : r]

def main():
    s = sys.stdin.readline().rstrip("\n")
    if not s:
        print()
        return
    best = s[0]
    n = len(s)
    for i in range(n):
        for pal in (expand(s, i, i), expand(s, i, i + 1)):
            if len(pal) > len(best) or (len(pal) == len(best) and pal < best):
                best = pal
    print(best)

if __name__ == "__main__":
    main()
