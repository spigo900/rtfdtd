import random

from dtd import roll_dice, calculate_value, stress_check_for_bad_things


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
