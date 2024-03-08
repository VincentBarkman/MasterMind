import random
import os

COLORS = {
    "R": {"name": "red", "code": "\033[91mR\033[0m"},
    "G": {"name": "green", "code": "\033[92mG\033[0m"},
    "B": {"name": "blue", "code": "\033[94mB\033[0m"},
    "Y": {"name": "yellow", "code": "\033[93mY\033[0m"},
    "M": {"name": "magenta", "code": "\033[95mM\033[0m"},
    "C": {"name": "cyan", "code": "\033[96mC\033[0m"},
}


def map_input_to_colors(input_list):
    return [COLORS[color.upper()]["name"] for color in input_list if color.upper() in COLORS]


def generate_code(colors, length=4):
    return random.choices(list(colors.keys()), k=length)


def get_guess(length=4):
    while True:
        guess_input = input(f"Enter your guess with {length} colors (e.g., R G B Y or RGBY for red green blue yellow): ").upper(
        ).replace(" ", "").strip()
        if len(guess_input) == length and all(char in COLORS for char in guess_input):
            return map_input_to_colors(guess_input)
        else:
            print(
                f"Invalid input. Please enter exactly {length} colors from the available list using their initials.")


def evaluate_guess(guess, code):
    mapped_code = map_input_to_colors(code)
    correct_positions = sum(g == c for g, c in zip(guess, mapped_code))
    correct_colors = sum(min(guess.count(c), mapped_code.count(c))
                         for c in set(guess)) - correct_positions
    return correct_positions, correct_colors


def display_board(attempts, max_attempts):
    print("\n\033[1mAttempts:\033[0m")
    os.system('cls' if os.name == 'nt' else 'clear')
    for attempt, feedback in attempts:
        guess_str = " ".join([COLORS[color[0].upper()]["code"]
                             for color in attempt])
        feedback_str = "✓" * feedback[0] + "?" * feedback[1]
        print(f"{guess_str} | Feedback: {feedback_str}")
    print("-" * 60)
    print("Available colors:", " ".join(
        [color["code"] for color in COLORS.values()]))


def main():
    code_length = 4
    max_attempts = code_length + 2
    code = generate_code(COLORS, code_length)

    attempts = []

    print("\033[1mWelcome to Mastermind!\033[0m\n")
    print("Available colors:", " ".join(
        [color["code"] for color in COLORS.values()]), "\n")
    print(
        f"Guess the correct sequence of {code_length} colors. You have {max_attempts} attempts.\n")
    print("Feedback symbols: ✓ = Correct color in the correct position, ? = Correct color in the wrong position.\n")

    for attempt in range(max_attempts):
        guess = get_guess(code_length)
        correct_positions, correct_colors = evaluate_guess(guess, code)
        attempts.append((guess, (correct_positions, correct_colors)))
        display_board(attempts, max_attempts)

        if correct_positions == code_length:
            print("\033[92mYou've guessed the correct sequence!\033[0m")
            return

        print(f"Attempt {attempt + 1}/{max_attempts}.")

    print("\033[91mYou've run out of attempts.\033[0m")
    print("The correct sequence was:", " ".join(
        [COLORS[color]["code"] for color in code]))


if __name__ == "__main__":
    main()
