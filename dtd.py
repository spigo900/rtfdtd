"""
Dice rolling and calculations for Past Due.
"""
import random
from typing import Sequence


SIDES = 10
D100_SIDES = 100


def roll_d100() -> int:
    """
    Roll a single d100 die.
    """
    return random.randint(1, D100_SIDES)


def roll_die(*, explodes: bool = True) -> int:
    """
    Roll a die, optionally exploding when we roll a 10.
    """
    result = roll = random.randint(1, SIDES)
    if explodes:
        while roll == SIDES:
            roll = random.randint(1, SIDES)
            result += roll
    return result


def roll_dice(n_roll: int, *, explodes: bool) -> Sequence[int]:
    """
    Roll the given number of dice, returning the rolls.
    """
    return [roll_die(explodes=explodes) for _ in range(n_roll)]


def calculate_value(rolls: Sequence[int], n_keep: int, *, attributes: str = "") -> int:
    """
    Calculate the value of a dice roll, given the rolls and number to keep.
    """
    print("CALCULATING VALUE")
    in_order = sorted(rolls)
    effective_negatives = max(attributes.count("-") - attributes.count("o"), 0)
    add_mod = 4 * (attributes.count("+") - effective_negatives)

    return _apply_mul(sum(in_order[-n_keep:]) + add_mod, attributes=attributes)

def _apply_mul(value_plus_add_mod: int, *, attributes: str) -> int:
    mul_offset = attributes.count("x") - attributes.count("/")
    if mul_offset > 0:
        return 2 * mul_offset * value_plus_add_mod
    elif mul_offset == 0:
        return value_plus_add_mod
    else:
        print(f"value is {value_plus_add_mod}")
        return value_plus_add_mod // (3 * -mul_offset)
