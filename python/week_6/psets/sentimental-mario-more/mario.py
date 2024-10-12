def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass


def print_pyramids(height):
    for i in range(1, height + 1):
        # Left pyramid
        print(" " * (height - i), end="")
        print("#" * i, end="")

        # Gap between pyramids
        print("  ", end="")

        # Right pyramid
        print("#" * i)


def main():
    height = get_height()
    print_pyramids(height)


main()
