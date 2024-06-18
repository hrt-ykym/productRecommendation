from dataclasses import dataclass


@dataclass
class Hello:
    def __init__(self, name: str):
        self.name = name

    def say(self) -> str:
        return f"Hello, {self.name}!"