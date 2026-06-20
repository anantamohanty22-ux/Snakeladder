"""Snake and Ladder game core logic.

Simple, dependency-free implementation suitable for CLI use.
"""
import random
from typing import Dict, List, Optional


class Board:
    SIZE = 100

    def __init__(self, snakes: Optional[Dict[int, int]] = None, ladders: Optional[Dict[int, int]] = None):
        # Default classic-ish board positions
        self.snakes = snakes or {
            16: 6,
            48: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78,
        }
        self.ladders = ladders or {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100,
        }

    def apply_snakes_ladders(self, pos: int) -> int:
        """Return new position after applying snake or ladder (if any)."""
        if pos in self.ladders:
            return self.ladders[pos]
        if pos in self.snakes:
            return self.snakes[pos]
        return pos


class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.position = 0
        self.is_ai = is_ai

    def __repr__(self):
        return f"Player({self.name!r}, pos={self.position})"


class Game:
    WIN_POS = Board.SIZE

    def __init__(self, players: List[Player], board: Optional[Board] = None, seed: Optional[int] = None):
        if len(players) < 2:
            raise ValueError("Need at least two players")
        self.players = players
        self.board = board or Board()
        self.current = 0
        self.winner: Optional[Player] = None
        if seed is not None:
            random.seed(seed)

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def play_turn(self, player: Player, roll: Optional[int] = None) -> dict:
        """Play a single turn for `player`.

        If `roll` is provided it's used (helpful for tests). Returns a dict with details.
        """
        if roll is None:
            roll = self.roll_dice()

        start = player.position
        tentative = start + roll

        # must land exactly on WIN_POS
        if tentative > self.WIN_POS:
            new_pos = start
        else:
            new_pos = self.board.apply_snakes_ladders(tentative)

        player.position = new_pos

        if player.position == self.WIN_POS:
            self.winner = player

        return {
            "player": player,
            "roll": roll,
            "start": start,
            "end": player.position,
            "winner": player if player.position == self.WIN_POS else None,
        }

    def next_player_index(self) -> int:
        self.current = (self.current + 1) % len(self.players)
        return self.current

    def play(self, verbose: bool = True):
        """Play until there is a winner. Prints progress when `verbose` is True."""
        while self.winner is None:
            player = self.players[self.current]
            if verbose:
                print(f"{player.name}'s turn (pos {player.position})")

            result = self.play_turn(player)
            if verbose:
                print(f"  rolled {result['roll']} -> {result['end']}")
                if result['end'] != result['start'] + result['roll'] and result['end'] != result['start']:
                    # landed on snake or ladder
                    if result['end'] > result['start'] + result['roll']:
                        print(f"  climbed a ladder to {result['end']}")
                    else:
                        print(f"  bitten by a snake to {result['end']}")

            if self.winner:
                if verbose:
                    print(f"\n{self.winner.name} wins!")
                return self.winner

            self.next_player_index()

        return self.winner


if __name__ == "__main__":
    # quick demo when running the module directly
    p1 = Player("Alice")
    p2 = Player("Bob", is_ai=True)
    game = Game([p1, p2])
    game.play()
