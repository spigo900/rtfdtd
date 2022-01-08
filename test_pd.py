import random

from past_due import handle_focus_for_roll, roll_dice, calculate_value, stress_check_for_bad_things


def test_roll_die():
    random.seed(42)
    rolls = roll_dice(1, explodes=True)
    assert len(rolls) == 1
    assert rolls[0] == 2


def test_roll_dice():
    random.seed(42)
    rolls = roll_dice(10, explodes=True)
    assert len(rolls) == 10
    assert rolls[0] == 2


def test_calculate_value():
    assert calculate_value([1, 1, 1, 6, 6, 6], 6) == 21
    assert calculate_value([1, 1, 1, 6, 6, 6], 3) == 18
    assert calculate_value([6, 6, 6, 1, 4, 2], 3) == 18
    assert calculate_value([10, 6, 6, 1, 4, 2], 3) == 22
    assert calculate_value([6, 10, 6, 1, 4, 2], 3) == 22
    assert calculate_value([1, 1, 1, 6, 6, 6], 1) == 6
    assert calculate_value([6, 6, 6, 1, 4, 2], 1) == 6
    assert calculate_value([10, 6, 6, 1, 4, 2], 1) == 10
    assert calculate_value([6, 10, 6, 1, 4, 2], 1) == 10


def test_calculate_value_with_simple():
    assert calculate_value([1, 1, 1, 6, 6, 6], 6, attributes="-") == 17
    assert calculate_value([1, 1, 1, 6, 6, 6], 3, attributes="+") == 22
    assert calculate_value([6, 6, 6, 1, 4, 2], 3, attributes="o") == 18
    assert calculate_value([10, 6, 6, 1, 4, 2], 3, attributes="x") == 44
    assert calculate_value([6, 10, 6, 1, 4, 2], 3, attributes="/") == 7
    assert calculate_value([1, 1, 1, 6, 6, 6], 1, attributes="//") == 1
    assert calculate_value([6, 6, 6, 1, 4, 2], 1, attributes="xx") == 24
    assert calculate_value([10, 6, 6, 1, 4, 2], 1, attributes="++") == 18
    assert calculate_value([6, 10, 6, 1, 4, 2], 1, attributes="--") == 2


def test_calculate_value_with_modifiers():
    assert calculate_value([1, 1, 1, 6, 6, 6], 6, attributes="/") == 7
    assert calculate_value([1, 1, 1, 6, 6, 6], 3, attributes="-/") == 4
    assert calculate_value([6, 6, 6, 1, 4, 2], 3, attributes="-") == 14
    assert calculate_value([10, 6, 6, 1, 4, 2], 3, attributes="---o+") == 18
    assert calculate_value([6, 10, 6, 1, 4, 2], 3, attributes="o") == 22
    assert calculate_value([1, 1, 1, 6, 6, 6], 1, attributes="o+") == 10
    assert calculate_value([6, 6, 6, 1, 4, 2], 1, attributes="x") == 12
    assert calculate_value([10, 6, 6, 1, 4, 2], 1, attributes="x//") == 3
    assert calculate_value([6, 10, 6, 1, 4, 2], 1, attributes="xx/") == 20


def test_calculate_value_with_stress():
    assert not stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 6, attributes="")
    assert not stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 6, attributes="s")
    assert stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 3, attributes="s")
    assert stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 3, attributes="s-/")
    assert stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 2, attributes="s-/")
    assert not stress_check_for_bad_things([1, 1, 1, 6, 6, 6], 4, attributes="s-/")
    assert not stress_check_for_bad_things([1, 1, 6, 6, 6, 6], 3, attributes="s-/")
    assert not stress_check_for_bad_things([6, 10, 6, 1, 4, 2], 3, attributes="s")


def test_calculate_value_with_stress():
    original_rolls = (1, 1, 12, 2, 6, 6)
    focus_roll = handle_focus_for_roll(original_rolls, attributes="")
    assert focus_roll.rolls == original_rolls
    assert focus_roll.phenomenality == 0

    focus_roll = handle_focus_for_roll(original_rolls, attributes="f")
    assert focus_roll.rolls == (1, 1, 11, 1, 6, 6)
    assert focus_roll.phenomenality == 2
