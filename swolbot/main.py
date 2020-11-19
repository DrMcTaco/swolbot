import os
from random import randint
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

from swolbot.users import BrodinUser
from swolbot.penance import Penance



intents = discord.Intents.default()
intents.members = True

description = "Tell brodin what has happend and he shall task you with penance."

bot = commands.Bot(command_prefix="/", description=description, intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if message.content.startswith("$hello"):
        logger.info(message)
        await message.channel.send(f"Hello {message.author}!")

#TODO: Get penance to persist so status works
@bot.group(name="swolbot", invoke_without_command=True)
async def swolbot(ctx, user: discord.Member, action):
    if ctx.invoked_subcommand is None:
        user = BrodinUser.get(user)
        if action.lower() == "died":
            task = Penance("pushups", reps=randint(5, 10))
            user.penance.append(task)
            await ctx.send(
                f"{user.user.mention} {action}! Brodin demands you {task.demand}!"
            )
        else:
            task = Penance("plank", reps=randint(3, 6) * 10)
            user.penance.append(task)
            await ctx.send(
                "Brodin does not recognize {action} as an action. Brodin demands you {task.demand}!"
            )


@swolbot.command(name="status")
async def _status(ctx, user: Optional[discord.Member]):
    if not user:
        user = ctx.message.author
    user = BrodinUser.get(user)
    message = f"{user.user.mention} is in Brodin's good grace."
    logger.info(user.penance)
    if user.unfinished_penance:
        penance_str = ", ".join(user.unfinished_penance)
        message = f"{user.user.mention} shall {penance_str} to please Brodin."
    await ctx.send(message)


load_dotenv()
bot.run(os.environ["BOT_TOKEN"])
