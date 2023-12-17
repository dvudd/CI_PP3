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


class PrintText:
    """
    Provides methods for displaying text on the screen.
    """

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def _calculate_pos(self, x_offset, y_offset, text):
        """
        Calculates the position of the text relative to the center
        of the screen
        """
        max_y, max_x = self.stdscr.getmaxyx()
        center_y, center_x = max_y // 2, max_x // 2
        y_pos = max(0, min(center_y + y_offset, max_y - 1))
        x_pos = max(0, min(center_x + x_offset - len(text) // 2, max_x - len(text)))
        return x_pos, y_pos

    def row(self, x_offset, y_offset, text, color=0, attribute=curses.A_NORMAL):
        """
        Displays text on the screen at a position relative to
        the center of the screen. Clears the entire row before printing
        """
        x_pos, y_pos = self._calculate_pos(x_offset, y_offset, text)
        self.stdscr.addstr(y_pos, 0, " " * self.stdscr.getmaxyx()[1])
        self.stdscr.addstr(y_pos, x_pos, text, curses.color_pair(color) | attribute)

        return x_pos

    def word(self, x_offset, y_offset, text, color=0, attribute=curses.A_NORMAL):
        """
        Displays text on the screen at a position relative to
        the center of the screen. Does not clear before printing
        """
        x_pos, y_pos = self._calculate_pos(x_offset, y_offset, text)
        self.stdscr.addstr(y_pos, x_pos, text, curses.color_pair(color) | attribute)


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
    scr = PrintText(stdscr)

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
            y_offset = i - 1
            scr.row(0, y_offset, rows[i])

            # Color code user input
            for j, char in enumerate(entry[i]):
                if j < len(rows[i]) and char == rows[i][j]:
                    color = 1
                    attribute = curses.A_NORMAL
                else:
                    color = 2
                    attribute = curses.A_UNDERLINE
                # Print the user input
                scr.word(
                    j - len(rows[i]) // 2,
                    y_offset,
                    char,
                    color,
                    attribute
                    )

        # Move cursor position
        cursor_y = center_y - 1 + pos_y
        if pos_y != 1:
            cursor_x = pos_x + (max_x - len(rows[pos_y])) // 2
        else:
            cursor_x = pos_x + center_x
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
                    entry[pos_y] = entry[pos_y][:pos_x] + entry[pos_y][pos_x + 1 :]
                elif pos_y > 0 and entry[pos_y - 1]:
                    pos_y -= 1
                    pos_x = len(entry[pos_y])

            # Printable character handling
            elif len(key) == 1 and key.isprintable():
                if pos_x < len(rows[pos_y]):
                    entry[pos_y] = entry[pos_y][:pos_x] + key + entry[pos_y][pos_x:]
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
        if start_time:
            remaining_time = max(int(end_time - time.time()), 0)
            # Print the timer
            scr.row(-30, -5, str(f"{remaining_time}s"), 3)
            scr.row(0, 8, " ")
        else:
            remaining_time = timer
            # Print the timer, but dimmed to indicate
            # that it is not active
            scr.row(-30, -5, str(f"{remaining_time}s"), 3, curses.A_DIM)
            # Print a short instruction
            scr.row(0, 8, "The test begins when you start typing", 0, curses.A_DIM)

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
    scr = PrintText(stdscr)
    stdscr.clear()
    while True:
        # Show the logo
        scr.row(0, -5, "░█▀▄░█▀▀░█▀▀░█░█░█░░░▀█▀░█▀▀")
        scr.row(0, -4, "░█▀▄░█▀▀░▀▀█░█░█░█░░░░█░░▀▀█")
        scr.row(0, -3, "░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀")

        # Print the net wpm result
        scr.word(0, 0, f"WPM: {net_wpm:.2f}")
        scr.word(2, 0, f"{net_wpm:.2f}", 3)
        scr.word(0, 1, f"Accuracy: {accuracy:.0f}%")
        scr.word(5, 1, f"{accuracy:.0f}%", 3)
        scr.word(0, 3, f"Gross WPM: {gross_wpm:.2f}")

        # Print the instructions
        scr.row(0, 8, "Press the Enter key to return to main menu", 0, curses.A_DIM)

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
    scr = PrintText(stdscr)
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
        scr.row(0, -5, "░█▀▀░█▀█░█▀▀░█▀▀░█▀▄░▀█▀░█░█░█▀█░█▀▀")
        scr.row(0, -4, "░▀▀█░█▀▀░█▀▀░█▀▀░█░█░░█░░░█░░█▀▀░█▀▀")
        scr.row(0, -3, "░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀░░░▀░░░▀░░▀░░░▀▀▀")

        # Display the instuctions to the user
        scr.row(0, 8, "Navigate through the menu using the arrow keys", 0, curses.A_DIM)
        scr.row(0, 9, "Confirm your selection with the Enter key", 0, curses.A_DIM)

        # Display the menu
        for idx, option in enumerate(options):
            y_offset = idx - (len(options) // 2) + 1
            if idx == current_option:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            scr.row(0, y_offset, option, 0, mode)

        # Display the current timer length
        scr.word(10, 1, "      ")
        scr.word(8, 1, f"[{timer}s]", 3)

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
                gross_wpm, net_wpm = calculate_wpm(num_correct, num_incorrect, timer)
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
