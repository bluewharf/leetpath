import sys


def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    st: list[str] = []
    for c in s:
        if c in pairs:
            if not st or st[-1] != pairs[c]:
                return False
            st.pop()
        else:
            st.append(c)
    return not st


def main() -> None:
    s = sys.stdin.readline().rstrip("\r\n")
    print("true" if is_valid(s) else "false")


if __name__ == "__main__":
    main()
