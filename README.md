# Title

## User Stories

## Features

## Development

## Testing
### Validator Testing

### Manual Testing

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


## Credits
- 500 most common words: https://www.summerboardingcourses.com/blogs/500-most-common-words-in-english/
- https://docs.python.org/3/library/curses.html
- Detect backspace: https://stackoverflow.com/questions/47481955/python-curses-detecting-the-backspace-key
- WPM Calculator: https://www.typingtyping.com/wpm-calculator/ **NOT IMPLEMENTED**
- python docs: https://docs.python.org/3/howto/curses.html
    - Attributes and Color: https://docs.python.org/3/howto/curses.html#attributes-and-color
    - isprintable: https://docs.python.org/3/library/stdtypes.html?highlight=isprintable#str.isprintable

### Acknowledgements	
- Thank you to my mentor Jack Wachira.\
![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)\
This is my Portfolio Project 3 as part of the Full Stack Software Developer program at [Code Institute](https://codeinstitute.net/).\
David Eriksson 2023