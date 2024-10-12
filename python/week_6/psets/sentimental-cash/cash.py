from cs50 import get_float


def main():
    # Prompt user for the amount of change owed
    while True:
        change = get_float("Change owed: ")
        if change >= 0:
            break

    # Convert dollars to cents to avoid floating-point issues
    cents = round(change * 100)

    # Initialize coin count
    coins = 0

    # Calculate the minimum number of coins
    coins += cents // 25  # Quarters
    cents %= 25

    coins += cents // 10  # Dimes
    cents %= 10

    coins += cents // 5   # Nickels
    cents %= 5

    coins += cents        # Pennies

    # Print the total number of coins
    print(coins)


main()
