import sys


def add_strings(a: str, b: str) -> str:
    if a == "":
        a = "0"
    if b == "":
        b = "0"
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        x = ord(a[i]) - 48 if i >= 0 else 0
        y = ord(b[j]) - 48 if j >= 0 else 0
        s = x + y + carry
        out.append(str(s % 10))
        carry = s // 10
        i -= 1
        j -= 1
    while len(out) > 1 and out[-1] == "0":
        out.pop()
    return "".join(reversed(out))


def main() -> None:
    a = sys.stdin.readline()
    b = sys.stdin.readline()
    a = a[:-1] if a.endswith("\n") else a
    b = b[:-1] if b.endswith("\n") else b
    print(add_strings(a, b))


if __name__ == "__main__":
    main()
