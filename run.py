# Write your code to expect a terminal of 80 characters wide and 24 rows high
import curses
import random


def get_random_string(length=10):
    """
    This will return 10 random words from the words file.
    """
    file = "words.txt"
    with open(file, 'r') as file:
        words = file.read().splitlines()
    
    random_words = random.sample(words, min(length, len(words)))

    return " ".join(random_words) + " "


def speed_test(stdscr):
    """
    This the game loop, it will present random words and check if the user types the correct
    character, changing it's color to green/red
    """
    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()

    # Generate two rows of random words
    rows = [""] + [get_random_string() for _ in range(2)]
    # Initialize a list to store the user's input
    user_input = ["" for _ in range(3)]
    # Set the starting position in them middle row
    pos = 1
    while True:
        # Display rows
        for i in range(3):
            stdscr.addstr(i, 0, rows[i])

        # Display user input, color green if correct or red if incorrect
        for i in range(3):
            stdscr.addstr(i, 0, rows[i])
            for j in range(len(user_input[i])):
                correct = rows[i][j] if j < len(rows[i]) else " "
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
            elif pos > 0 and rows[pos - 1]:
                # Move to the previous row
                pos -= 1
        # Check if input is a printable character
        elif len(key) == 1 and key.isprintable():
            user_input[pos] += key
            if len(user_input[pos]) == len(rows[pos]):
                # Once row1 is completed, move back to row2
                if pos == 0:
                    pos = 1

        # Shift rows up and load a new row
        if len(user_input[1]) == len(rows[1]):
            # Clear the screen to avoid 
            stdscr.clear()
            # Move row2 to row1, row3 to row2
            rows[:2] = rows[1:]
            # Generate a new row at row3
            rows[2] = get_random_string()
            # Shift user_input
            user_input[:2] = user_input[1:]
            # New empty string for row3
            user_input[2] = ""
            # Keep typing on row2
            pos = 1

        # Refresh the screen
        stdscr.refresh()


def main():
    curses.wrapper(speed_test)


if __name__ == "__main__":
    main()
