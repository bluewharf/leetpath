import sys


def multiply(a: str, b: str) -> str:
    a = a.strip()
    b = b.strip()
    if a == "0" or b == "0":
        return "0"
    n, m = len(a), len(b)
    pos = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            pos[(n - 1 - i) + (m - 1 - j)] += (ord(a[i]) - 48) * (ord(b[j]) - 48)
    carry = 0
    for k in range(len(pos)):
        s = pos[k] + carry
        pos[k] = s % 10
        carry = s // 10
    while carry:
        pos.append(carry % 10)
        carry //= 10
    while len(pos) > 1 and pos[-1] == 0:
        pos.pop()
    return "".join(str(d) for d in reversed(pos))


def main() -> None:
    a = sys.stdin.readline()
    b = sys.stdin.readline()
    print(multiply(a, b))


if __name__ == "__main__":
    main()
