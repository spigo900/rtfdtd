"""
Dice rolling and calculations for Past Due.
"""
import random
from typing import Sequence


SIDES = 10


def roll_dice(n_roll: int) -> Sequence[int]:
    """
    Roll the given number of dice, returning the rolls.
    """
    return [random.randint(1, SIDES + 1) for _ in range(n_roll)]


def calculate_value(rolls: Sequence[int], n_keep: int) -> int:
    """
    Calculate the value of a dice roll, given the rolls and number to keep.
    """
    in_order = sorted(rolls)
    return sum(in_order[-n_keep:])
