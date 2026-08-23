import sys


def main() -> None:
    s = sys.stdin.readline().rstrip("\n")
    best = 0
    st = [-1]
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
    print(best)


if __name__ == "__main__":
    main()
