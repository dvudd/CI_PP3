import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import calculate_wpm

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
    gross_wpm, net_wpm = calculate_wpm(50, 100, 60)
    assert gross_wpm == 30
    assert net_wpm == -70