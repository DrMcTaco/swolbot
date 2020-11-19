from dataclasses import dataclass, field
from typing import List

from discord import Member
import discord

from swolbot.penance import Penance

USERS = {}


@dataclass
class BrodinUser:
    user: Member
    penance: List[Penance] = field(default_factory=list)

    def __post_init__(self):
        USERS.update({self.user.id: self})

    @classmethod
    def get(cls, user: discord.Member):
        return USERS.get(user.id, cls(user))

    @property
    def unfinished_penance(self):
        return [penance for penance in self.penance if not penance.completed]