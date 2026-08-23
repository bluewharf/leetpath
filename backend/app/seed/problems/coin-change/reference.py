import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    coins = list(map(int, data[1 : 1 + n]))
    amount = int(data[1 + n])
    inf = amount + 1
    dp = [inf] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        if coin > amount:
            continue
        for x in range(coin, amount + 1):
            cand = dp[x - coin] + 1
            if cand < dp[x]:
                dp[x] = cand
    print(-1 if dp[amount] >= inf else dp[amount])


if __name__ == "__main__":
    main()
