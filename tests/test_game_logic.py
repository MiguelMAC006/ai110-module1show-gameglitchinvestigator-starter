from logic_utils import check_guess, parse_guess, get_range_for_difficulty


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: Hint directions were swapped ---
# Original bug: guess > secret returned "Go HIGHER!" (wrong), guess < secret returned "Go LOWER!" (wrong)

def test_too_high_message_says_go_lower():
    # When guess is above the secret, the message must tell the player to go LOWER
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' hint but got: {message}"


def test_too_low_message_says_go_higher():
    # When guess is below the secret, the message must tell the player to go HIGHER
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' hint but got: {message}"


# --- Bug 2: Secret was alternately cast to str, breaking integer comparisons ---
# Original bug: on even attempts app.py passed str(secret) to check_guess,
# causing string-vs-int comparisons that produced wrong outcomes.

def test_check_guess_with_integer_secret():
    # Must work correctly with integer secret (not accidentally coerced to str)
    outcome, _ = check_guess(99, 50)
    assert outcome == "Too High"

def test_check_guess_int_not_confused_by_string_coercion():
    # Simulates the old bug: passing str(secret) would cause wrong comparison
    # e.g. str comparison "9" > "50" is True because "9" > "5" lexicographically
    outcome_correct, _ = check_guess(9, 50)   # 9 < 50 → Too Low (correct int comparison)
    assert outcome_correct == "Too Low"


# --- Bug 3: parse_guess should handle decimal strings and empty/None input ---

def test_parse_guess_decimal_string():
    ok, value, _ = parse_guess("42.7")
    assert ok is True
    assert value == 42

def test_parse_guess_empty_string():
    ok, _, error = parse_guess("")
    assert ok is False
    assert error == "Enter a guess."

def test_parse_guess_none():
    ok, _, error = parse_guess(None)
    assert ok is False
    assert error == "Enter a guess."

def test_parse_guess_non_numeric():
    ok, _, error = parse_guess("abc")
    assert ok is False
    assert error == "That is not a number."

def test_parse_guess_valid_integer():
    ok, value, error = parse_guess("37")
    assert ok is True
    assert value == 37
    assert error is None


# --- get_range_for_difficulty ---

def test_difficulty_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

def test_difficulty_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 100)

def test_difficulty_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 50)
