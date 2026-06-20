"""Command-line runner for the Snake and Ladder game."""
from src.snake_ladder import Game, Player


def prompt_int(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if v < min_v or v > max_v:
                print(f"Enter a number between {min_v} and {max_v}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")


def main():
    print("Snake and Ladder - CLI")
    n = prompt_int("Number of players (2-6): ", 2, 6)
    players = []
    for i in range(1, n + 1):
        name = input(f"Name for player {i}: ").strip() or f"P{i}"
        typ = input("Type (h)uman or (a)i? [h]: ").strip().lower() or "h"
        is_ai = typ.startswith("a")
        players.append(Player(name, is_ai=is_ai))

    game = Game(players)
    print("Starting game. First to reach 100 wins. Exact roll required to land on 100.")
    game.play()


if __name__ == "__main__":
    main()
