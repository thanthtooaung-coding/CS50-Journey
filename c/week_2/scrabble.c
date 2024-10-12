#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int calculate_word_score(string word);

int main(void)
{
    // Prompt for the user for two words
    string player1_word = get_string("Player 1: ");
    string player2_word = get_string("Player 2: ");

    // Compute the score of each word
    int player1_score = calculate_word_score(player1_word);
    int player2_score = calculate_word_score(player2_word);

    // Print the winner
    if (player1_score > player2_score)
    {
        printf("Player 1 wins!\n");
    }
    else if (player2_score > player1_score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int calculate_word_score(string word)
{
    int total_score = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isalpha(word[i]))
        {
            total_score += POINTS[toupper(word[i]) - 'A'];
        }
    }
    return total_score;
}
