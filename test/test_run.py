import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import calculate_wpm, calculate_accuracy, get_random_string

def test_calculate_wpm():
    # Test case all correct characters for 30 seconds
    gross_wpm, net_wpm = calculate_wpm(200, 0, 30)
    assert gross_wpm == 80
    assert net_wpm == 80

    # Test case all correct characters for 1 minute
    gross_wpm, net_wpm = calculate_wpm(200, 0, 60)
    assert gross_wpm == 40
    assert net_wpm == 40

    # Test case all correct characters for 2 minutes
    gross_wpm, net_wpm = calculate_wpm(200, 0, 120)
    assert gross_wpm == 20
    assert net_wpm == 20

    # Test case with some correct and incorrect characters
    gross_wpm, net_wpm = calculate_wpm(100, 20, 60)
    assert gross_wpm == 24
    assert net_wpm == 4

    # Test case with more incorrect characters than correct
    # It should not return a negative value.
    gross_wpm, net_wpm = calculate_wpm(50, 100, 60)
    assert gross_wpm == 30
    assert net_wpm == 0

def test_calculate_accuracy():
    # All correct characters
    assert calculate_accuracy(100, 0) == 100.0

    # Some incorrect but mostly correct characters
    assert calculate_accuracy(80, 20) == 80.0

    # Equal number of correct and incorrect characters
    assert calculate_accuracy(50, 50) == 50.0
    
    # All incorrect characters
    assert calculate_accuracy(0, 100) == 0.0

    # Edge case: No characters typed
    assert calculate_accuracy(0, 0) == 0.0

def test_get_random_string():
    # With no argument, returned words should be 10
    random_words = get_random_string()
    assert len(random_words.split()) == 10

    # With a argument of 100
    random_words = get_random_string(100)
    assert len(random_words.split()) == 100

    # With a argument of 0
    random_words = get_random_string(0)
    assert len(random_words.split()) == 0