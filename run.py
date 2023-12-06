# Write your code to expect a terminal of 80 characters wide and 24 rows high
import curses
import random


def get_random_string(length=10):
    """
    This will return random words from the words list.
    I will probably not do this in the final version, time will tell.
    """
    words = [
        "hello",
        "world",
        "this",
        "is",
        "a",
        "typing",
        "test",
        "to",
        "see",
        "if",
        "heroku",
        "can",
        "handle",
        "curses",
    ]
    return " ".join(random.choice(words) for _ in range(length)) + " "


def speed_test(stdscr):
    """
    This the game loop, it will present random words and check if the user types the correct
    character, changing it's color to green/red
    """
    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()

    # Generate three rows of random words
    rows = [get_random_string() for _ in range(3)]
    # Initialize a list to store the user's input
    user_input = ["" for _ in range(3)]

    pos = 0
    while True:
        # Display rows
        for i in range(3):
            stdscr.addstr(i, 0, rows[i])

        # Display user input, color green if correct or red if incorrect
        for i in range(3):
            for j in range(len(user_input[i])):
                correct = rows[i][j]
                current_string = user_input[i][j]
                color_pair = 1 if current_string == correct else 2
                attribute = (
                    curses.A_NORMAL if current_string == correct else curses.A_UNDERLINE
                )
                stdscr.addch(
                    i, j, current_string, curses.color_pair(color_pair) | attribute
                )

        # Move the cursor
        stdscr.move(pos, len(user_input[pos]))

        # Listen for keyboard presses
        key = stdscr.getkey()

        # Detect backspace
        if key in ["KEY_BACKSPACE", "\b", "\x7f"]:
            if len(user_input[pos]) > 0:
                user_input[pos] = user_input[pos][:-1]
            elif pos > 0:
                pos -= 1
                user_input[pos] = user_input[pos][:-1]
        else:
            # Add user input to the user_input list
            user_input[pos] += key

        # Move to next row if current row is completed
        if len(user_input[pos]) == len(rows[pos]):
            # Ensure pos does not exceed 2
            pos = min(pos + 1, 2)

        # Refresh the screen
        stdscr.refresh()


def main():
    curses.wrapper(speed_test)


if __name__ == "__main__":
    main()
