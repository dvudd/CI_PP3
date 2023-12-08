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
    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()

    # Initialize counters and cursor positions
    correct_chars = 0
    incorrect_chars = 0

    # Initialize cursor position, start in the middle row
    pos_y, pos_x = 1, 0

    # Initialize list of user input
    user_input = ["" for _ in range(3)]

    # Generate two rows of random words
    rows = [""] + [get_random_string() for _ in range(2)]

    while True:
        # Display rows and color code user input
        for i in range(3):
            stdscr.addstr(i, 0, rows[i])
            for j in range(len(user_input[i])):
                is_correct = j < len(rows[i]) and user_input[i][j] == rows[i][j]
                color_pair = 1 if is_correct else 2
                attribute = curses.A_NORMAL if is_correct else curses.A_UNDERLINE
                stdscr.addch(i, j, user_input[i][j], curses.color_pair(color_pair) | attribute)

        # Move the cursor
        stdscr.move(pos_y, pos_x)

        # Listen for keyboard presses
        key = stdscr.getkey()

        # Backspace handling
        if key in ["KEY_BACKSPACE", "\b", "\x7f"]:
            if pos_x > 0:
                pos_x -= 1
                last_char_correct = user_input[pos_y][pos_x] == rows[pos_y][pos_x]
                user_input[pos_y] = user_input[pos_y][:pos_x] + user_input[pos_y][pos_x+1:]
                if last_char_correct:
                    correct_chars -= 1
                else:
                    incorrect_chars -= 1
            elif pos_y > 0 and user_input[pos_y - 1]:
                pos_y -= 1
                pos_x = len(user_input[pos_y])
       
        # Printable character handling
        elif len(key) == 1 and key.isprintable():
            if pos_x < len(rows[pos_y]):
                user_input[pos_y] = user_input[pos_y][:pos_x] + key + user_input[pos_y][pos_x:]
                is_correct = key == rows[pos_y][pos_x]
                if is_correct:
                    correct_chars += 1
                else:
                    incorrect_chars += 1
                pos_x += 1

                # Move cursor back to middle row after completing the top row
                if pos_y == 0 and pos_x == len(rows[pos_y]):
                    pos_y = 1
                    pos_x = len(user_input[pos_y])

        # Row completion and shifting logic
        if pos_y == 1 and pos_x >= len(rows[pos_y]):
            rows.pop(0)
            rows.append(get_random_string())
            user_input.pop(0)
            user_input.append("")
            pos_x = 0

        # REMOVE THIS, ONLY FOR TESTING
        stdscr.clear()
        stdscr.addstr(5, 0, str(correct_chars), curses.color_pair(1))
        stdscr.addstr(6, 0, str(incorrect_chars), curses.color_pair(2))

        # Refresh the screen
        stdscr.refresh()


def main():
    curses.wrapper(speed_test)


if __name__ == "__main__":
    main()
