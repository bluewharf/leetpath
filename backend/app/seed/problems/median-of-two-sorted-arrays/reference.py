import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1 : n + 1]
    m = data[n + 1]
    b = data[n + 2 : n + 2 + m]
    i = j = 0
    merged: list[int] = []
    while i < n and j < m:
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    tot = n + m
    mid = tot // 2
    if tot % 2:
        med = float(merged[mid])
    else:
        med = (merged[mid - 1] + merged[mid]) / 2.0
    print(f"{med:.1f}")


if __name__ == "__main__":
    main()
