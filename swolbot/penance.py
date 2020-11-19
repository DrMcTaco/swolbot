from dataclasses import dataclass
from enum import Enum


class Excercise(Enum):
    pushups = "pushups"
    crunches = "crunches"
    squats = "squats"
    plank = "plank"


@dataclass
class Penance:
    excercise: Excercise
    reps: int
    completed: bool = False

    @property
    def demand(self):
        if self.excercise == Excercise.plank:
            return f"{self.excercise} for {self.reps} seconds"
        return f"do {self.reps} {self.excercise}"