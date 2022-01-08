"""
A Discord bot that rolls dice for Past Due.
"""
import json
from pathlib import Path

import discord

from dtd import roll_d100, roll_dice, calculate_value


CONFIG_PATH = Path("./config.json")

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

    if message.content.startswith("/roll"):
        parts = message.content.lower().strip().split()
        roll_expr = parts[1]

        if "k" in parts[1]:
            n_roll, n_keep = [int(subexpr) for subexpr in roll_expr.split("k")]
            on_roll(message, n_roll, n_keep)
        elif parts[1] == "d100":
            on_d100(message)


async def on_roll(message: discord.Message, n_roll: int, n_keep: int) -> None:
    """
    Logic for the d10-rolling parts of the /roll command.

    This handles rolling things like skill checks.
    """
    rolls = roll_dice(n_roll, explodes=True)
    value = calculate_value(rolls, n_keep)
    message.channel.send(
        f"Rolled: {value}\n\n"
        f"(sorted rolls {', '.join(sorted(rolls))} || roll order {', '.join(rolls)})"
    )


async def on_d100(message: discord.Message, n_roll: int, n_keep: int) -> None:
    """
    Logic for the d100/percentile-rolling parts of the /roll command.

    This handles things like rolling credit checks, or rolling on the Wizard's
    Twilight table.
    """
    message.channel.send(f"Rolled d100: {roll_d100()}")


if __name__ == "__main__":
    with CONFIG_PATH.open("r", encoding="utf-8") as json_in:
        config = json.load(json_in)
    client.run(config["token"])
