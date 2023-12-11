# Write your code to expect a terminal of 80 characters wide and 24 rows high
import curses
import random
import time


def get_random_string(length=10):
    """
    This will return 10 random words from the words file.
    """
    file = "words.txt"
    with open(file, 'r') as file:
        words = file.read().splitlines()
    
    random_words = random.sample(words, min(length, len(words)))

    return " ".join(random_words) + " "


def speed_test(stdscr, timer_length=30):
    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.nodelay(True)

    # Initialize counters and cursor positions
    correct_chars = 0
    incorrect_chars = 0
    start_time = None
    end_time = None

    # Initialize cursor position, start in the middle row
    pos_y, pos_x = 1, 0

    # Initialize list of user input
    user_input = ["" for _ in range(3)]

    # Generate two rows of random words
    rows = [""] + [get_random_string() for _ in range(2)]

    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        middle_y = max_y // 2
        center_x = max(0, (max_x - len(rows[1])) // 2)
        
        # Display rows of text
        for i in range(3):
            y_position = middle_y - 1 + i
            x_position = center_x if i == 1 else (max_x - len(rows[i])) // 2
            # Clear the row before printing
            stdscr.addstr(y_position, 0, " " * max_x)
            # Print the row
            stdscr.addstr(y_position, x_position, rows[i])

            # Display user input with color coding
            for j in range(len(user_input[i])):
                is_correct = j < len(rows[i]) and user_input[i][j] == rows[i][j]
                color_pair = 1 if is_correct else 2
                attribute = curses.A_NORMAL if is_correct else curses.A_UNDERLINE
                stdscr.addch(y_position, j + x_position, user_input[i][j], curses.color_pair(color_pair) | attribute)

        # Move cursor position
        cursor_y = middle_y - 1 + pos_y
        cursor_x = pos_x + (center_x if pos_y == 1 else (max_x - len(rows[pos_y])) // 2)
        stdscr.move(cursor_y, cursor_x)

        # Listen for keyboard presses
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

        if key:
            # Start the timer once user presses a key
            if start_time is None:
                start_time = time.time()
                end_time = start_time + timer_length

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

        # Display the remaing time
        if start_time:
            remaining_time = max(int(end_time - time.time()), 0)
        else:
            remaining_time = timer_length
        # Clear the text before printing
        stdscr.addstr(y_position - 5, 0, " " * max_x)
        # Print the timer
        stdscr.addstr(y_position - 5,  max_x // 2 - 30, str(f"{remaining_time}s"), curses.color_pair(3))

        # Check if the time is up
        if remaining_time <= 0:
            break

    return correct_chars, incorrect_chars


def main():
    curses.wrapper(speed_test)


if __name__ == "__main__":
    main()
