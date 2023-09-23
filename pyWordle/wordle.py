import random
from rich.console import Console
from rich.theme import Theme
from string import ascii_letters, ascii_lowercase
from datamuse import Datamuse

console = Console(width=40, theme=Theme({
    "warning": "red on yellow",
}), color_system="windows")

api = Datamuse()


def main():
    word = get_random_word()
    guess_list = ['_' * 5] * 6
    refresh('Welcome to My Game')
    for number in range(6):
        refresh(headline=f"Guess: {number + 1}")
        guess = get_guess(guess_list)
        guess_list[number] = guess
        show_guesses(guess_list, word)
        if guess == word:
            console.print(f"[green]Amazing![/],the word is :grinning_face_with_sweat:[blue]{word}[/]")
            break

    else:
        print_sol(word)


def get_random_word():
    letter = f"{random.choice(ascii_lowercase)}????"
    results = api.suggest(s=letter, max_results=1)
    word = random.choice([item['word'] for item in results])
    return word


def get_guess(previous):
    guess = console.input(f"\nEnter Guess:")

    if guess in previous:
        console.print(f"You have already guessed {guess}!", style='warning')
        return get_guess(previous)
    if len(guess) != 5:
        console.print('Your guess must be five letters', style='warning')
        return get_guess(previous)

    return guess


def show_guess(guess, word):
    correct = {letter for letter, correct_letter in zip(guess, word) if letter == correct_letter}
    incorrect = set(guess) - set(word)
    misplaced = set(guess) & set(word) - correct

    print("Correct letters:", ", ".join(sorted(correct)))
    print("Misplaced letters:", ", ".join(sorted(misplaced)))
    print("Wrong letters:", ", ".join(sorted(incorrect)))


def show_guesses(guess_list, word):
    for guess in guess_list:
        styling = []
        for guess_letter, correct_letter in zip(guess, word):
            if guess_letter == correct_letter:
                style = "#FFFFFF on green"
            elif guess_letter in word:
                style = "#FFFFFF on yellow"
            elif guess_letter in ascii_letters:
                style = "#FFFFFF on #666666"
            else:
                style = "dim"
            styling.append(f"[{style}]{guess_letter.upper()}[/]")
        console.print("".join(styling), justify="center")


def refresh(headline):
    console.rule(f":snake: [bold blue][leafy green] {headline} [leafy green] :snake:[/]\n")


def print_sol(word):
    console.print(f"Game over! The word was [bold blue on #FFFFFF]{word}[/]")


if __name__ == '__main__':
    main()
