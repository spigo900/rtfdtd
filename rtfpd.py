"""
A Discord bot that rolls dice for Past Due.
"""
import json
from pathlib import Path

import discord

from past_due import (
    roll_d100,
    roll_dice,
    calculate_value,
    stress_check_for_bad_things,
    calculate_focus_roll,
)


CONFIG_PATH = Path("./config.json")
# N keep M notation (e.g. 6k2) is undocumented 'cause it's legacy :P
HELP = """Commands: !roll (aka !r), !help

- Use !r X Y [attributes] to make a normal Past Due roll.
- Use !r d100 to roll a d100.

Use 'o' for the ⊕ attribute."""
NAUGHTY = "... Nice try."
BAD_ROLL_COMMAND = """Unrecognized roll command syntax.

Reminder: syntax is !r X Y [attributes] or !r d100."""

client = discord.Client()


@client.event
async def on_ready() -> None:
    "Hook for when the Discord API finishes setup?"
    print(f"Logged in as {client.user}.")


@client.event
async def on_message(message: discord.Message) -> None:
    "Hook for when anyone in a participating guild sends a message."
    if not message.content.startswith("!"):
        return

    if message.content.startswith("!help"):
        await message.channel.send(HELP)
    elif message.content.startswith("!roll") or message.content.startswith("!r"):
        print(f"Got roll command: {message.content}")
        parts = message.content.lower().strip().split()

        # Command is of the form !r X Y attributes
        if len(parts) == 4:
            raw_x, raw_y, attributes = parts[1:]
            x, y = int(raw_x), int(raw_y)  # pylint: disable=invalid-name
            n_roll, n_keep = max(x, y), min(x, y)
            if sanity_check_roll(n_roll, n_keep, attributes=attributes):
                await on_roll(message, n_roll, n_keep, attributes=attributes)
            else:
                await message.channel.send(NAUGHTY)
        # Command looks like !r 6k2. (Legacy command.)
        elif "k" in parts[1]:
            n_roll, n_keep = [int(subexpr) for subexpr in parts[1].split("k")]
            attributes = parts[2] if len(parts) >= 3 else ""
            if sanity_check_roll(n_roll, n_keep, attributes=attributes):
                await on_roll(message, n_roll, n_keep, attributes=attributes)
            else:
                await message.channel.send(NAUGHTY)
        # Command looks like d100
        elif parts[1] == "d100":
            await on_d100(message)
        else:
            await message.channel.send(BAD_ROLL_COMMAND)


def sanity_check_roll(n_roll: int, n_keep: int, *, attributes: str = "") -> bool:
    """
    Check if the given roll command is reasonable so we don't get DoSed. :)
    """
    return -10 <= n_roll <= 10 and -9 <= n_keep <= 9 and len(attributes) < 20


async def on_roll(
    message: discord.Message, n_roll: int, n_keep: int, *, attributes: str
) -> None:
    """
    Logic for the d10-rolling parts of the /roll command.

    This handles rolling things like skill checks.
    """
    base_rolls = roll_dice(n_roll, explodes=n_keep > 0)
    focus_roll = calculate_focus_roll(base_rolls, attributes)
    bad_things = stress_check_for_bad_things(focus_roll.rolls, n_keep, attributes=attributes)
    value = calculate_value(focus_roll.rolls, n_keep, attributes=(2 ** focus_roll.phenomenality) * attributes)
    flag_messages = []
    if focus_roll.phenomenality > 0:
        flag_messages.append(
            f"phenomal! {focus_roll.phenomenality} twos. "
            f"twos rerolled per dice: "
            f"{', '.join(str(count) for count in focus_roll.reroll_counts)}"
        )
    if bad_things:
        flag_messages.append("stress, bad things!")
    reply = (
        f"Rolled: {value}{' (' + ' '.join(flag_messages) + ')' if flag_messages else ''}\n\n"
        f"(sorted rolls {', '.join(str(roll) for roll in sorted(focus_roll.rolls, reverse=True))}\n"
        f"| roll order {', '.join(str(roll) for roll in focus_roll.rolls)}"
    )
    if focus_roll.phenomenality > 0:
        reply += (
            f"\n| before applying F attribute "
            f"{', '.join(str(roll) for roll in base_rolls)})"
        )
    else:
        reply += ")"
    await message.channel.send(reply)


async def on_d100(message: discord.Message) -> None:
    """
    Logic for the d100/percentile-rolling parts of the /roll command.

    This handles things like rolling credit checks, or rolling on the Wizard's
    Twilight table.
    """
    await message.channel.send(f"Rolled d100: {roll_d100()}")


if __name__ == "__main__":
    with CONFIG_PATH.open("r", encoding="utf-8") as json_in:
        config = json.load(json_in)
    client.run(config["token"])
