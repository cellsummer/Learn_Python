def main():
    print(fib(6))


# memorization
def fib(n):
    # initialization
    memo = {0: 0, 1: 1}

    def helper(n):
        if n not in memo:
            memo[n] = helper(n - 1) + helper(n - 2)
        return memo[n]

    return helper(n)


if __name__ == "__main__":
    main()
