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
    with open(file, 'r') as file:
        words = file.read().splitlines()
    
    random_words = random.sample(words, min(length, len(words)))

    return " ".join(random_words) + " "


def speed_test(stdscr, timer_length):
    """
    This is the main game loop, it will present rows of texts to the user
    and color the user input green/red depending if it is correct or not.
    The timer starts to count down as soon as the user starts typing.
    The function will return the number och correct / incorrect characters after
    the loop.
    """
    # Clear the screen and show the cursor
    stdscr.clear()

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

    # Game Loop
    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        center_y = max_y // 2
        center_x = max(0, (max_x - len(rows[1])) // 2)
        
        # Display rows of text
        for i in range(3):
            y_position = center_y - 1 + i
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
        cursor_y = center_y - 1 + pos_y
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
        # Clear the text before printing
        stdscr.addstr(y_position - 5, 0, " " * max_x)
        stdscr.addstr(y_position + 8, 0, " " * max_x)
        if start_time:
            remaining_time = max(int(end_time - time.time()), 0)
            # Print the remaining time
            stdscr.addstr(y_position - 5,  max_x // 2 - 30, str(f"{remaining_time}s"), curses.color_pair(3))
        else:
            remaining_time = timer_length
            # Dim the remaining time and show a short instruction
            attribute = curses.A_DIM
            stdscr.addstr(y_position - 5,  max_x // 2 - 30, str(f"{remaining_time}s"), curses.color_pair(3) | attribute)
            stdscr.addstr(y_position + 8, center_x + 8, "The test begins when you start typing", curses.A_DIM)

        # Check if the time is up
        if remaining_time <= 0:
            break

    return correct_chars, incorrect_chars

def calculate_wpm(correct_chars, incorrect_chars, timer_length):
    """
    Here the WPM (Words Per Minute) is calculated. The function will return both
    the Gross and Net WPM values.
    """
    all_chars = correct_chars + incorrect_chars
    gross_wpm = (all_chars / 5) / (timer_length / 60)
    net_wpm = gross_wpm - (incorrect_chars / (timer_length / 60))

    return gross_wpm, net_wpm

def calculate_accuracy(correct_chars, incorrect_chars):
    """
    Here we calculate the accuracy of the users input.
    """
    all_chars = correct_chars + incorrect_chars
    # Prevent division by zero
    if all_chars == 0:
        return 0
    accuracy = (correct_chars / all_chars) * 100

    return accuracy

def main(stdscr):
    """
    Main menu, here the user gets the option to set the timer duration, start the game or exit.
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
    timer_length = 30
    # Timer options
    timer_options = [30, 60, 120, 180]
    # Index for timer
    timer_option_index = 0

    # Menu Loop
    while True:
        # Calculate center positions
        max_y, max_x = stdscr.getmaxyx()
        center_y = max_y // 2
        center_x = max(0, (max_x // 2))

        # Show the logo
        stdscr.addstr(center_y - 5, center_x - (36 // 2), "░█▀▀░█▀█░█▀▀░█▀▀░█▀▄░▀█▀░█░█░█▀█░█▀▀")
        stdscr.addstr(center_y - 4, center_x - (36 // 2), "░▀▀█░█▀▀░█▀▀░█▀▀░█░█░░█░░░█░░█▀▀░█▀▀")
        stdscr.addstr(center_y - 3, center_x - (36 // 2), "░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀░░░▀░░░▀░░▀░░░▀▀▀")

        # Display the instuctions to the user
        stdscr.addstr(center_y + 8, center_x - 18, "Navigate through the menu using the arrow keys", curses.A_DIM)
        stdscr.addstr(center_y + 9, center_x - 15, "Confirm your selection with the Enter key", curses.A_DIM)

        # Display the menu
        for idx, option in enumerate(options):
            y_position = center_y + idx
            mode = curses.A_REVERSE if idx == current_option else curses.A_NORMAL
            stdscr.addstr(y_position, center_x - 4, option, mode)

        # Display the current timer length
        stdscr.addstr(center_y + 1, center_x + 10, "      ")
        stdscr.addstr(center_y + 1, center_x + 6, f"[{timer_length}s]", curses.color_pair(3))

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
        elif key in ['\n', '\r']:
            # Start the game, display the results afterward
            if current_option == 0:
                correct_chars, incorrect_chars = speed_test(stdscr, timer_length)
                # Calculate WPM and accuracy
                gross_wpm, net_wpm = calculate_wpm(correct_chars, incorrect_chars, timer_length)
                accuracy = calculate_accuracy(correct_chars, incorrect_chars)
                # Display the results
                stdscr.clear()
                stdscr.addstr(center_y + 5, center_x - 18, f"Gross WPM:")
                stdscr.addstr(center_y + 5, center_x - 7, f"{gross_wpm:.2f}", curses.color_pair(3))
                stdscr.addstr(center_y + 6, center_x - 16, f"Net WPM:")
                stdscr.addstr(center_y + 6, center_x - 7, f"{net_wpm:.2f}", curses.color_pair(3))
                stdscr.addstr(center_y + 5, center_x + 4, f"accuracy:")
                stdscr.addstr(center_y + 5, center_x + 14, f"{accuracy:.2f}%", curses.color_pair(3))
                stdscr.refresh()
            # Switch trough the timer options
            elif current_option == 1:
                timer_option_index = (timer_option_index + 1) % len(timer_options)
                timer_length = timer_options[timer_option_index]
            # Exit the program
            elif current_option == 2:
                break


if __name__ == "__main__":
    curses.wrapper(main)