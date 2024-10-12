#include <cs50.h>
#include <stdio.h>

void print_hashes(int count);

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print the pyramid
    for (int i = 1; i <= height; i++)
    {
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        print_hashes(i);

        printf("  ");

        print_hashes(i);

        printf("\n");
    }
}

void print_hashes(int count)
{
    for (int i = 0; i < count; i++)
    {
        printf("#");
    }
}
