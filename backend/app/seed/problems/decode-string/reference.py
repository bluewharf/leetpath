import sys


def decode_string(s: str) -> str:
    num_stack: list[int] = []
    str_stack: list[list[str]] = []
    cur: list[str] = []
    k = 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + ord(ch) - 48
        elif ch == "[":
            num_stack.append(k)
            str_stack.append(cur)
            cur = []
            k = 0
        elif ch == "]":
            prev = str_stack.pop()
            n = num_stack.pop()
            cur = prev + cur * n
        else:
            cur.append(ch)
    return "".join(cur)


def main() -> None:
    s = sys.stdin.readline().rstrip("\r\n")
    print(decode_string(s))


if __name__ == "__main__":
    main()
