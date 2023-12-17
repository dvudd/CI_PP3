# SPEEDTYPE
[SPEEDTYPE](https://wpm-test-cf8ee303cbf2.herokuapp.com/)
## User Stories

## Features

## Development

## Testing
### Validator Testing
The code is validated with [CI Python Linter](https://pep8ci.herokuapp.com/#) with no errors or warnings.

**RESULTS**

### Manual Testing
| Element | Expected Behavior | Outcome |
| ------- | ------------------ | ------- |
| Main Menu | Shows at the beginning | Confirmed |
| Main Menu | Shows logo | Confirmed |
| Main Menu | Shows the instructions at the bottom | Confirmed |
| Main Menu | Shows the three menu options | Confirmed |
| Main Menu | UP and DOWN arrows navigate through the options | Confirmed |
| Main Menu | Pressing ENTER on the timer options changes the timer | Confirmed |
| Main Menu | Pressing ENTER on the Quit option exits the program | Confirmed |
| Main Menu | Pressing ENTER on the Start Game option starts the game | Confirmed |
| Game | Shows two rows of randomly selected words | Confirmed |
| Game | The cursor is on the first letter of the first word | Confirmed |
| Game | The timer is the one selected from the main menu | Confirmed |
| Game | The timer does not count down and is dimmed | Confirmed |
| Game | Shows the instructions at the bottom | Confirmed |
| Game | The timer starts when first button is pressed | Confirmed |
| Game | The timer is now not dimmed | Confirmed |
| Game | The instructions disappear once the timer starts | Confirmed |
| Game | The timer counts down regardless of user input | Confirmed |
| Game | The cursor moves the the right when input is entered | Confirmed |
| Game | The letter turns green if input is correct | Confirmed |
| Game | The letter turns red if input is incorrect | Confirmed |
| Game | The letter is highlighted with and underscore if input is incorrect | Confirmed |
| Game | The cursor moves the the left when backspace is pressed | Confirmed |
| Game | The letter turns white when backspacing | Confirmed |
| Game | When the last letter of the row is entered, the row moves up one position | Confirmed |
| Game | When row is complete the cursor moves back to the start | Confirmed |
| Game | When row is complete a new row of words are printed below | Confirmed |
| Game | When backspacing I can move back to the previous row | Confirmed |
| Game | The game ends when the timer reaches 0 | Confirmed |
| Results | Shows the RESULT logo | Confirmed |
| Results | Shows the results in the middle | Confirmed |
| Results | Shows the instructions at the bottom | Confirmed |
| Results | Pressing ENTER the Main menu is showed again | Confirmed |
| Error handling | The program exits if the terminal window is too small | Confirmed |
| Error handling | The program exits if the words.txt is not found | Confirmed |

### Automated Testing
To verify that the calculations are correct I set up automated tests using [pytest](https://docs.pytest.org/en/7.4.x/). These tests are in the `test_run.py` in the `test` folder.

To install `pytest`, issue the command `pip3 install pytest`. Once the installation is complete run the command `pytest test`.

**RESULTS**

## Bugs
<details><summary>BUG: Rows are not separated by whitespace</summary>
The last word of one row and the first word of the next row is not separated by whitespace, making it easy to misspell. This was fixed by adding a whitespace in the end of the `get_random_string` function

```python
return " ".join(random.choice(words) for _ in range(length))
```
to
```python
return " ".join(random.choice(words) for _ in range(length)) + " "
```

</details>
<details><summary>BUG: When user presses TAB or the arrow keys it gets processed as a valid input.</summary>
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

</details>
<details><summary>BUG: Shows incorrect coloring and text when the rows are shifted.</summary>
This was corrected by clearing the screen and before moving the rows

```python        # Shift rows up and load a new row
        if len(user_input[1]) == len(rows[1]):
            # Clear the screen to avoid 
            stdscr.clear()
```

</details>
<details><summary>BUG: User can backspace into empty row</summary>
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

</details>
<details><summary>BUG: Old text stays on screen when it should have been removed</summary>
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

</details>
<details><summary>BUG: ZeroDivisionError in calculate_accuracy function</summary>
This occured when no characters are typed in and the calculate_accuracy function tries to divide by zero.
To prevent this I added this check before the division:

```python
if all_chars == 0:
    return 0
```

</details>
<details><summary>BUG: curses.error: curs_set() returned ERR when deployed on Heroku</summary>

This bug occured when the project was deployed on Heroku. According to this [Bug Report](https://github.com/isontheline/pro.webssh.net/issues/709) there's a problem with certain terminal settings and hiding the cursor. Since it doesn't seem like I can change the terminal settings in Heroku I did a workaround to hide the cursor behind the highlighted option in main menu.

```python
# Hide the cursor behind the highlighted menu option
cursor_y = center_y + current_option
cursor_x = center_x - len(options[current_option]) // 2
stdscr.move(cursor_y, cursor_x)
```

</details>
<details><summary>BUG: Cursor is sometimes on the wrong position on a new row</summary>
This bug occured because how the position of the rows of text and the position of the cursor where
calculated seperatly and it was not certain that the to calculations came up with the same result.

To fix this I saved the row starting position in a list and use that as the cursors starting position.
```python
# Keep track of the row starting positions
start_pos = []
# Display rows of text
for i in range(3):
    y_offset = i - 1
    x_pos = scr.row(0, y_offset, rows[i])
    start_pos.append(x_pos)
# Calculate center positions
max_y, max_x = stdscr.getmaxyx()
center_y = max_y // 2

# Move cursor position
cursor_x = start_pos[pos_y] + len(entry[pos_y])
cursor_x = min(cursor_x, max_x - 1)
cursor_y = center_y - 1 + pos_y
stdscr.move(cursor_y, cursor_x)
```

</details>
<details><summary>BUG: Cursor is on the wrong position when backspacing back to the top row</summary>
This bug occured on how I implemented the row positioning and how the the python len() function works. Basicly it adds an extra whitespace at the end of the row, to fix this I simply remove that trailing whitespace.

```python
# Move the cursor to the top row
elif pos_y > 0 and entry[pos_y - 1]:
    pos_y -= 1
    entry[pos_y] = entry[pos_y].rstrip()
    pos_x = len(entry[pos_y])
```

</details>

## Credits
- 1000 most common words: https://github.com/powerlanguage/word-lists
- https://docs.python.org/3/library/curses.html
- Detect backspace: https://stackoverflow.com/questions/47481955/python-curses-detecting-the-backspace-key
- Get screen size: https://stackoverflow.com/questions/53019526/get-updated-screen-size-in-python-curses
- WPM Calculator: https://www.speedtypingonline.com/typing-equations
- ASCII Art Generator: https://www.asciiart.eu/text-to-ascii-art
- Handle file not found: https://stackoverflow.com/questions/22366282/python-filenotfound
- python docs: https://docs.python.org/3/howto/curses.html
    - Attributes and Color: https://docs.python.org/3/howto/curses.html#attributes-and-color
    - isprintable: https://docs.python.org/3/library/stdtypes.html?highlight=isprintable#str.isprintable
    - getmaxyx: https://docs.python.org/3/library/curses.html?highlight=getmaxyx#curses.window.getmaxyx
    - nodelay: https://docs.python.org/3/library/curses.html#curses.window.nodelay
    - refresh: https://docs.python.org/3/library/curses.html#curses.window.refresh
    - endwin: https://docs.python.org/3/library/curses.html#curses.endwin
### Acknowledgements	
- Thank you to my mentor Jack Wachira.\
![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)\
This is my Portfolio Project 3 as part of the Full Stack Software Developer program at [Code Institute](https://codeinstitute.net/).\
David Eriksson 2023