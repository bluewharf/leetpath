import sys


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    prices = data[1 : 1 + n]
    min_price = prices[0]
    best = 0
    for p in prices[1:]:
        profit = p - min_price
        if profit > best:
            best = profit
        if p < min_price:
            min_price = p
    print(best)


if __name__ == "__main__":
    main()
