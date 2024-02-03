from random import randint
from typing import Optional, TypeVar


class Die:
    """Class representing a die."""

    def __init__(self, num_sides: Optional[int] = 6) -> None:
        """
        Initialize the die with a specified number of sides.

        Args:
        num_sides (int): The number of sides for the die. Default is 6.
        """
        self.num_sides: int = num_sides

    def roll(self) -> int:
        """Returning a random roll from 1 to number of sides."""
        return randint(1, self.num_sides)
