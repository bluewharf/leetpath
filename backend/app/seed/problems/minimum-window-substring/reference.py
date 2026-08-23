import sys
from collections import Counter


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    t = sys.stdin.readline().rstrip("\n")
    need = Counter(t)
    required = len(need)
    formed = 0
    window: dict[str, int] = {}
    left = 0
    best_len = 10**18
    best_l = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1
        while left <= right and formed == required:
            cur = right - left + 1
            if cur < best_len:
                best_len = cur
                best_l = left
            cl = s[left]
            window[cl] -= 1
            if cl in need and window[cl] < need[cl]:
                formed -= 1
            left += 1
    if best_len == 10**18:
        print()
    else:
        print(s[best_l : best_l + best_len])


if __name__ == "__main__":
    main()
