# Write your code to expect a terminal of 80 characters wide and 24 rows high
import curses
import random
import time


def get_random_string(length=10):
    """
    This will return random words from the words file.
    The number of words can be modified by the argument.
    Default is 10 words.
    """
    file = "words.txt"
    with open(file, "r") as file:
        words = file.read().splitlines()

    random_words = random.sample(words, min(length, len(words)))

    return " ".join(random_words) + " "


def speed_test(stdscr, timer):
    """
    This is the main game loop, it will present rows of texts to the user
    and color the user input green/red depending if it is correct or not.
    The timer starts to count down as soon as the user starts typing.
    The function will return the number och correct / incorrect characters
    after the loop.
    """
    # Clear the screen and show the cursor
    stdscr.clear()

    # Initialize counters and cursor positions
    num_correct = 0
    num_incorrect = 0
    start_time = None
    end_time = None

    # Initialize cursor position, start in the middle row
    pos_y, pos_x = 1, 0

    # Initialize list of user input
    entry = ["" for _ in range(3)]

    # Generate two rows of random words
    rows = [""] + [get_random_string() for _ in range(2)]

    # Game Loop
    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        center_y = max_y // 2
        center_x = max(0, (max_x - len(rows[1])) // 2)

        # Display rows of text
        for i in range(3):
            y_position = center_y - 1 + i
            if i == 1:
                x_position = center_x
            else:
                x_position = (max_x - len(rows[i])) // 2
            # Clear the row before printing
            stdscr.addstr(y_position, 0, " " * max_x)
            # Print the row
            stdscr.addstr(y_position, x_position, rows[i])

            # Color code user input
            for j in range(len(entry[i])):
                if j < len(rows[i]) and entry[i][j] == rows[i][j]:
                    color_pair = 1
                    attribute = curses.A_NORMAL
                else:
                    color_pair = 2
                    attribute = curses.A_UNDERLINE
                # Print the user input
                stdscr.addch(
                    y_position,
                    j + x_position,
                    entry[i][j],
                    curses.color_pair(color_pair) | attribute,
                )

        # Move cursor position
        cursor_y = center_y - 1 + pos_y
        if pos_y == 1:
            cursor_x = pos_x + center_x
        else:
            cursor_x = pos_x + (max_x - len(rows[pos_y])) // 2
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
                end_time = start_time + timer

            # Backspace handling
            if key in ["KEY_BACKSPACE", "\b", "\x7f"]:
                if pos_x > 0:
                    pos_x -= 1
                    if entry[pos_y][pos_x] == rows[pos_y][pos_x]:
                        num_correct -= 1
                    else:
                        num_incorrect -= 1
                    entry[pos_y] = (
                        entry[pos_y][:pos_x] + entry[pos_y][pos_x + 1:]
                    )
                elif pos_y > 0 and entry[pos_y - 1]:
                    pos_y -= 1
                    pos_x = len(entry[pos_y])

            # Printable character handling
            elif len(key) == 1 and key.isprintable():
                if pos_x < len(rows[pos_y]):
                    entry[pos_y] = (
                        entry[pos_y][:pos_x] + key + entry[pos_y][pos_x:]
                    )
                    if key == rows[pos_y][pos_x]:
                        num_correct += 1
                    else:
                        num_incorrect += 1
                    pos_x += 1

                    # Move cursor back to middle row after
                    # completing the top row
                    if pos_y == 0 and pos_x == len(rows[pos_y]):
                        pos_y = 1
                        pos_x = len(entry[pos_y])

            # Row completion and shifting logic
            if pos_y == 1 and pos_x >= len(rows[pos_y]):
                rows.pop(0)
                rows.append(get_random_string())
                entry.pop(0)
                entry.append("")
                pos_x = 0

        # Display the remaing time
        # Clear the text before printing
        stdscr.addstr(y_position - 5, 0, " " * max_x)
        stdscr.addstr(y_position + 8, 0, " " * max_x)
        if start_time:
            remaining_time = max(int(end_time - time.time()), 0)
            # Print the timer
            stdscr.addstr(
                y_position - 5,
                max_x // 2 - 30,
                str(f"{remaining_time}s"),
                curses.color_pair(3),
            )
        else:
            remaining_time = timer
            # Print the timer, but dimmed to indicate
            # that it is not active
            attribute = curses.A_DIM
            stdscr.addstr(
                y_position - 5,
                max_x // 2 - 30,
                str(f"{remaining_time}s"),
                curses.color_pair(3) | attribute,
            )
            # Print a short instruction
            stdscr.addstr(
                y_position + 8,
                center_x + 8,
                "The test begins when you start typing",
                curses.A_DIM,
            )

        # Check if the time is up
        if remaining_time <= 0:
            break

    return num_correct, num_incorrect


def calculate_wpm(num_correct, num_incorrect, timer):
    """
    Here the WPM (Words Per Minute) is calculated.
    The function will return both the Gross and Net WPM values.
    """
    all_chars = num_correct + num_incorrect
    gross_wpm = (all_chars / 5) / (timer / 60)
    net_wpm = gross_wpm - (num_incorrect / (timer / 60))

    return gross_wpm, net_wpm


def calculate_accuracy(num_correct, num_incorrect):
    """
    Here we calculate the accuracy of the users input.
    """
    all_chars = num_correct + num_incorrect
    # Prevent division by zero
    if all_chars == 0:
        return 0
    accuracy = (num_correct / all_chars) * 100

    return accuracy


def show_results(stdscr, gross_wpm, net_wpm, accuracy, timer):
    """
    Presents the results to the user
    """
    # Clear the screen
    stdscr.clear()
    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        center_y = max_y // 2
        center_x = max(0, (max_x // 2))

        # Show the logo
        stdscr.addstr(
            center_y - 5,
            center_x - (28 // 2),
            "░█▀▄░█▀▀░█▀▀░█░█░█░░░▀█▀░█▀▀"
        )
        stdscr.addstr(
            center_y - 4,
            center_x - (28 // 2),
            "░█▀▄░█▀▀░▀▀█░█░█░█░░░░█░░▀▀█"
        )
        stdscr.addstr(
            center_y - 3,
            center_x - (28 // 2),
            "░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀"
        )

        # Print the net wpm result
        stdscr.addstr(center_y, center_x - 8, f"Net WPM:")
        stdscr.addstr(
            center_y,
            center_x + 1,
            f"{net_wpm:.2f}",
            curses.color_pair(3)
        )

        # Print the gross wpm result
        stdscr.addstr(center_y + 7, center_x - 20, f"Gross WPM:")
        stdscr.addstr(
            center_y + 7,
            center_x - 9,
            f"{gross_wpm:.2f}",
            curses.color_pair(3)
        )

        # Print the accuracy result
        stdscr.addstr(center_y + 7, center_x + 5, f"accuracy:")
        stdscr.addstr(
            center_y + 7,
            center_x + 15,
            f"{accuracy:.2f}%",
            curses.color_pair(3)
        )

        # Print the instructions
        stdscr.addstr(
            center_y + 9,
            center_x - 20,
            "Press the Enter key to return to main menu",
            curses.A_DIM,
        )

        # Hide the cursor in the top left corner
        stdscr.move(0, 0)

        # Wait for user input
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

        # Listen for the Enter key
        if key in ["\n", "\r"]:
            stdscr.clear()
            break


def main(stdscr):
    """
    Main menu, here the user gets the option to
    set the timer duration, start the game or exit.
    """
    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.nodelay(True)

    # Menu options
    options = ["Play Game", "Set Timer", "Quit"]
    # Index for menu
    current_option = 0

    # Default Timer
    timer = 30
    # Timer options
    timer_options = [30, 60, 120, 180]
    # Index for timer
    timer_index = 0

    # Menu Loop
    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        center_y = max_y // 2
        center_x = max(0, (max_x // 2))

        # Show the logo
        stdscr.addstr(
            center_y - 5,
            center_x - (36 // 2),
            "░█▀▀░█▀█░█▀▀░█▀▀░█▀▄░▀█▀░█░█░█▀█░█▀▀"
        )
        stdscr.addstr(
            center_y - 4,
            center_x - (36 // 2),
            "░▀▀█░█▀▀░█▀▀░█▀▀░█░█░░█░░░█░░█▀▀░█▀▀"
        )
        stdscr.addstr(
            center_y - 3,
            center_x - (36 // 2),
            "░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀░░░▀░░░▀░░▀░░░▀▀▀"
        )

        # Display the instuctions to the user
        stdscr.addstr(
            center_y + 8,
            center_x - 23,
            "Navigate through the menu using the arrow keys",
            curses.A_DIM,
        )
        stdscr.addstr(
            center_y + 9,
            center_x - 20,
            "Confirm your selection with the Enter key",
            curses.A_DIM,
        )

        # Display the menu
        for idx, option in enumerate(options):
            y_position = center_y + idx
            if idx == current_option:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            stdscr.addstr(y_position, center_x - 4, option, mode)

        # Display the current timer length
        stdscr.addstr(center_y + 1, center_x + 10, "      ")
        stdscr.addstr(
            center_y + 1,
            center_x + 6,
            f"[{timer}s]",
            curses.color_pair(3)
        )

        # Hide the cursor behind the highlighted menu option
        cursor_y = center_y + current_option
        cursor_x = center_x - len(options[current_option]) // 2
        stdscr.move(cursor_y, cursor_x)

        # Handle key presses
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

        # UP and ARROW keys flips trough menu
        if key == "KEY_UP" and current_option > 0:
            current_option -= 1
        elif key == "KEY_DOWN" and current_option < len(options) - 1:
            current_option += 1
        # Detect ENTER key
        elif key in ["\n", "\r"]:
            # Start the game, display the results afterward
            if current_option == 0:
                num_correct, num_incorrect = speed_test(stdscr, timer)
                # Calculate WPM and accuracy
                gross_wpm, net_wpm = calculate_wpm(
                    num_correct, num_incorrect, timer
                )
                accuracy = calculate_accuracy(num_correct, num_incorrect)
                # Display the results
                show_results(stdscr, gross_wpm, net_wpm, accuracy, timer)
            # Switch trough the timer options
            elif current_option == 1:
                timer_index = (timer_index + 1) % len(timer_options)
                timer = timer_options[timer_index]
            # Exit the program
            elif current_option == 2:
                break


if __name__ == "__main__":
    curses.wrapper(main)
