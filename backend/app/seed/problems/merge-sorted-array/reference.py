import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    idx = 0
    n = data[idx]
    idx += 1
    a = data[idx : idx + n]
    idx += n
    m = data[idx]
    idx += 1
    b = data[idx : idx + m]
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    print(" ".join(map(str, out)))


if __name__ == "__main__":
    main()
