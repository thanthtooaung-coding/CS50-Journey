#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Number: ");
    int sum1 = 0, sum2 = 0;
    int count = 0;
    long temp = number;

    while (temp > 0)
    {
        int digit = temp % 10;
        count++;

        if (count % 2 == 0)
        {
            int product = digit * 2;
            sum1 += product / 10 + product % 10;
        }
        else
        {
            sum2 += digit;
        }

        temp /= 10;
    }

    int total = sum1 + sum2;
    bool valid = (total % 10 == 0);

    if (valid)
    {
        long first_two_digits = number;
        while (first_two_digits >= 100)
        {
            first_two_digits /= 10;
        }

        if (count == 15 && (first_two_digits == 34 || first_two_digits == 37))
        {
            printf("AMEX\n");
        }
        else if (count == 16 && (first_two_digits >= 51 && first_two_digits <= 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((count == 13 || count == 16) && first_two_digits / 10 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
