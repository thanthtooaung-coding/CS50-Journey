from cs50 import get_string


def count_letters(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1
    return letters


def count_words(text):
    # Split the text by spaces to count words
    words = text.split()
    return len(words)


def count_sentences(text):
    sentences = 0
    for char in text:
        if char in ['.', '!', '?']:
            sentences += 1
    return sentences


def main():
    # Prompt the user for some text
    text = get_string("Text: ")

    # Count letters, words, and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the Coleman-Liau index
    L = letters / words * 100
    S = sentences / words * 100
    index = 0.0588 * L - 0.296 * S - 15.8

    # Print the grade level
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {round(index)}")


main()
