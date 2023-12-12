# Title

## User Stories

## Features

## Development

## Testing
### Validator Testing
The code is validated with [CI Python Linter](https://pep8ci.herokuapp.com/#) with no errors or warnings.

**RESULTS**

### Manual Testing

### Automated Testing
To verify that the calculations are correct I set up automated tests using [pytest](https://docs.pytest.org/en/7.4.x/). These tests are in the `test_run.py` in the `test` folder.

To install `pytest`, issue the command `pip3 install pytest`. Once the installation is complete run the command `pytest test`.

**RESULTS**

## Bugs
BUG: The last word of one row and the first word of the next row is not separated by whitespace, making it easy to misspell. This was fixed by adding a whitespace in the end of the `get_random_string` function
```python
return " ".join(random.choice(words) for _ in range(length))
```
to
```python
return " ".join(random.choice(words) for _ in range(length)) + " "
```

BUG: When user presses TAB or the arrow keys it gets processed as a valid input.
The issue was resolved by running the input through the `.isprintable()` function
```python
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
```
to:
```python
        # Detect backspace
        if key in ["KEY_BACKSPACE", "\b", "\x7f"]:
            if len(user_input[pos]) > 0:
                user_input[pos] = user_input[pos][:-1]
            elif pos > 0:
                pos -= 1
                user_input[pos] = user_input[pos][:-1]
        # Check if key is a printable character
        elif len(key) == 1 and key.isprintable():
            user_input[pos] += key
```

BUG: Shows incorrect coloring and text when the rows are shifted.
This was corrected by clearing the screen and before moving the rows
```python        # Shift rows up and load a new row
        if len(user_input[1]) == len(rows[1]):
            # Clear the screen to avoid 
            stdscr.clear()
```

BUG: User can backspace into empty row
This happen if the user backspaces into the top row while that row is still empty.
To correct this I added an extra condition to the backspace key.
From:
```python
elif pos > 0:
    # Move to the previous row
    pos -= 1
```
To:
```python
elif pos > 0 and rows[pos - 1]:
    # Move to the previous row
    pos -= 1
```

BUG: Old text stays on screen when it should have been removed
This could be resolved by using `stdscr.refresh()`, however this resulted in the cursor and text blinking in a high frequency. I opted to instead clear the rows of text and the timer before printing it out again.

From:
```python
for i in range(3):
    y_position = center_y - 1 + i
    x_position = center_x if i == 1 else (max_x - len(rows[i])) // 2
    stdscr.addstr(y_position, x_position, rows[i])

# Display the remaing time
if start_time:
    remaining_time = max(int(end_time - time.time()), 0)
else:
    remaining_time = timer_length
stdscr.addstr(y_position - 5,  max_x // 2 - 30, str(f"{remaining_time}s"), curses.color_pair(3))
```
To:
```python
for i in range(3):
    y_position = center_y - 1 + i
    x_position = center_x if i == 1 else (max_x - len(rows[i])) // 2
    # Clear the row before printing
    stdscr.addstr(y_position, 0, " " * max_x)
    # Print the row
    stdscr.addstr(y_position, x_position, rows[i])

# Display the remaing time
if start_time:
    remaining_time = max(int(end_time - time.time()), 0)
else:
    remaining_time = timer_length
# Clear the text before printing
stdscr.addstr(y_position - 5, 0, " " * max_x)
# Print the timer
stdscr.addstr(y_position - 5,  max_x // 2 - 30, str(f"{remaining_time}s"), curses.color_pair(3))
```

BUG: ZeroDivisionError in calculate_accuracy function
This occured when no characters are typed in and the calculate_accuracy function tries to divide by zero.
To prevent this I added this check before the division:
```python
if all_chars == 0:
    return 0
```

BUG: curses.error: curs_set() returned ERR when deployed on Heroku
This bug occured when the project was deployed on Heroku. According to this [Bug Report](https://github.com/isontheline/pro.webssh.net/issues/709) there's a problem with certain terminal settings and hiding the cursor. Since it seems I cant change the terminal settings in Heroku I did a workaround to hide the cursor behind the highlighted option in main menu.
```python
# Hide the cursor behind the highlighted menu option
cursor_y = center_y + current_option
cursor_x = center_x - len(options[current_option]) // 2
stdscr.move(cursor_y, cursor_x)
```

## Credits
- 1000 most common words: https://github.com/powerlanguage/word-lists
- https://docs.python.org/3/library/curses.html
- Detect backspace: https://stackoverflow.com/questions/47481955/python-curses-detecting-the-backspace-key
- Get screen size: https://stackoverflow.com/questions/53019526/get-updated-screen-size-in-python-curses
- WPM Calculator: https://www.speedtypingonline.com/typing-equations
- ASCII Art Generator: https://www.asciiart.eu/text-to-ascii-art
- python docs: https://docs.python.org/3/howto/curses.html
    - Attributes and Color: https://docs.python.org/3/howto/curses.html#attributes-and-color
    - isprintable: https://docs.python.org/3/library/stdtypes.html?highlight=isprintable#str.isprintable
    - getmaxyx: https://docs.python.org/3/library/curses.html?highlight=getmaxyx#curses.window.getmaxyx
    - nodelay: https://docs.python.org/3/library/curses.html#curses.window.nodelay
    - refresh: https://docs.python.org/3/library/curses.html#curses.window.refresh
### Acknowledgements	
- Thank you to my mentor Jack Wachira.\
![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)\
This is my Portfolio Project 3 as part of the Full Stack Software Developer program at [Code Institute](https://codeinstitute.net/).\
David Eriksson 2023