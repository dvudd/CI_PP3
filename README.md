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


## Credits
- https://docs.python.org/3/library/curses.html
- Detect backspace: https://stackoverflow.com/questions/47481955/python-curses-detecting-the-backspace-key
- WPM Calculator: https://www.typingtyping.com/wpm-calculator/ **NOT IMPLEMENTED**
- python docs: https://docs.python.org/3/howto/curses.html
    - Attributes and Color: https://docs.python.org/3/howto/curses.html#attributes-and-color

### Acknowledgements	
- Thank you to my mentor Jack Wachira.\
![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)\
This is my Portfolio Project 3 as part of the Full Stack Software Developer program at [Code Institute](https://codeinstitute.net/).\
David Eriksson 2023