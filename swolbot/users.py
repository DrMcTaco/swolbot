from dataclasses import dataclass, field
from typing import List

from discord import Member
import discord
from loguru import logger

from swolbot.penance import Penance

# Use a python dict as a users cache until I implement a DB
USERS = dict()


@dataclass
class BrodinUser:
    member: Member
    penance: List[Penance] = field(default_factory=list)

    def __post_init__(self):
        # put the user in the cache
        USERS[self.member.id] = self

    @classmethod
    def get(cls, member: discord.Member):
        user = USERS.get(member.id)
        if not user:
            user = cls(member)
        return user

    @property
    def unfinished_penance(self):
        return [penance for penance in self.penance if not penance.completed]