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
    return " ".join(random.choice(words) for _ in range(length))


def speed_test(stdscr):
    """
    This the game loop, it will present random words and check if the user types the correct
    character, changing it's color to green/red
    """
    random_string = get_random_string()
    current_string = [" "] * len(random_string)

    # Initialize curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.addstr(random_string + "\n")
    stdscr.refresh()

    pos = 0
    while True:
        # Listen for keyboard presses
        key = stdscr.getkey()
        # Detect backspace
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if pos > 0:
                pos -= 1
                current_string[pos] = " "
                stdscr.addstr(0, pos, random_string[pos], curses.color_pair(0))
                stdscr.move(0, pos)
        # Check if correct or not
        elif pos < len(random_string):
            correct = random_string[pos]
            current_string[pos] = key
            color = curses.color_pair(1) if key == correct else curses.color_pair(2)
            stdscr.addstr(0, pos, correct, color)
            pos += 1

        stdscr.refresh()

        if pos >= len(random_string):
            break


def main():
    curses.wrapper(speed_test)


if __name__ == "__main__":
    main()
