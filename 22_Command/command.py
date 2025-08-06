from abc import abstractmethod
from collections import deque

from pydantic import BaseModel


class Command():
    @abstractmethod
    def execute(self) -> None:
        pass


class MacroCommand(Command, BaseModel):
    commands: deque = deque()

    def execute(self):
        for command in self.commands:
            command.execute()

    def append(self, command: Command) -> None:
        if command == self:
            raise ValueError('infinite loop caused by append')
        self.commands.append(command)

    def undo(self) -> None:
        if self.commands:
            self.commands.pop()

    def clear(self) -> None:
        self.commands.clear()
