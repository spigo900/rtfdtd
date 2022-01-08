"""
Dice rolling and calculations for Past Due.
"""
from dataclasses import dataclass
from math import ceil
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
    Calculate the value of a dice roll, given the rolls, number to keep, and
    attributes.
    """
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
        return value_plus_add_mod // (3 * -mul_offset)


def stress_check_for_bad_things(
    rolls: Sequence[int], n_keep: int, *, attributes: str
) -> bool:
    """
    Check if Bad Things happen due to stress.

    This checks for the stress attribute; if it's not present then this always
    returns false.
    """
    return "s" in attributes and len(
        [x for x in rolls if x == 1]
    ) >= _num_ones_for_stress(len(rolls), n_keep)


def _num_ones_for_stress(n_roll: int, n_keep: int) -> int:
    """
    Calculate the minimum number of ones for a bad effect on a stressed roll.
    """
    return max(ceil(n_roll / 2), n_keep)


@dataclass(frozen=True)
class ResolvedFocusRoll:
    """
    Holds the result of resolving a focus (or phenomenon) roll.

    This includes the rerolls (as rolls) and the reroll counts for each die.
    It also includes the number of twos rolled in the rerolling process (the
    phenomenality).
    """
    rolls: Sequence[int]
    reroll_counts: Sequence[int]
    phenomenality: int


def calculate_focus_roll(rolls: Sequence[int], attributes: str) -> ResolvedFocusRoll:
    """
    Calculate the phenomenality of the given raw roll.

    For a focus roll (i.e. one with the F modifier), the phenomenality is
    the number of twos rolled. For all others the phenomenality is 0.
    """
    # Calculate phenomenality.
    #
    # I include "or 10" in case of non-exploding focus rolls.
    new_rolls = []
    reroll_counts = []
    phenomenality = 0
    if "f" in attributes:
        for roll in rolls:
            print()
            reroll = roll
            reroll_count = 0
            # Note that because rolls only explode on a 10, we can write
            # (re)roll = 10 * q + r, where q is the number of explosions
            # and 1 <= r < 10 is the last number rolled. Thus modding by 10 gives
            # us r, the last number rolled.
            while (reroll % 10) == 2:
                phenomenality += 1
                reroll_count += 1
                # Reroll with explosions... I assume that's how this is supposed to
                # work, because the rules don't say otherwise.
                die = roll_die(explodes=True)
                # Also subtract two to get rid of the 2 roll, which I believe
                # doesn't count towards the total.
                reroll += die - 2
            new_rolls.append(reroll)
            reroll_counts.append(reroll_count)
    else:
        new_rolls = rolls
        reroll_counts = [0 for _ in rolls]

    return ResolvedFocusRoll(
        rolls=tuple(new_rolls),
        reroll_counts=tuple(reroll_counts),
        phenomenality=phenomenality,
    )
