from gc import isenabled
import os
from random import randint
from re import U
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

@bot.group(name="swolbot", invoke_without_command=True, pass_context=True)
async def swolbot(ctx, user: discord.Member, action: str):
    if ctx.invoked_subcommand is None:
        user = BrodinUser.get(user)
        if action.lower() == "died":
            task = Penance("pushups", reps=randint(5, 10))
            user.penance.append(task)
            await ctx.send(
                f"{user.member.mention} {action}! Brodin demands you {task.demand}!"
            )
        else:
            task = Penance("plank", reps=randint(3, 6) * 10)
            user.penance.append(task)
            await ctx.send(
                "Brodin does not recognize {action} as an action. Brodin demands you {task.demand}!"
            )


@swolbot.command(name="status", pass_context=True)
async def _status(ctx, user: Optional[discord.Member]):
    if not user:
        user = ctx.message.author
    user = BrodinUser.get(user)
    message = f"{user.member.mention} is in Brodin's good grace."
    if user.unfinished_penance:
        penance_str = ", ".join([task.demand for task in user.unfinished_penance])
        message = f"{user.member.mention} shall {penance_str} to please Brodin."
    await ctx.send(message)
    breakpoint()
    logger.info(user.member.activities)


load_dotenv()
bot.run(os.environ["BOT_TOKEN"])
