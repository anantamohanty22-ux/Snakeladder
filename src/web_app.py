from flask import Flask, render_template, request, redirect, url_for, session
from uuid import uuid4
import os
import sys

# Ensure project root is on sys.path so `src` package imports work when running
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.snake_ladder import Game, Player

app = Flask(__name__)
app.secret_key = "dev-secret-for-local"  # fine for local dev

# Simple in-memory store for games keyed by id. Single-process only.
GAMES = {}


@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"]) 
def start():
    # Only allow exactly two players
    p1 = request.form.get("p1", "Player 1").strip() or "Player 1"
    p2 = request.form.get("p2", "Player 2").strip() or "Player 2"
    ai2 = request.form.get("ai2") == "on"

    players = [Player(p1, is_ai=False), Player(p2, is_ai=ai2)]
    game = Game(players)
    gid = str(uuid4())
    GAMES[gid] = game
    session["game_id"] = gid
    session.modified = True
    return redirect(url_for("game_view"))


@app.route("/game", methods=["GET"]) 
def game_view():
    gid = session.get("game_id")
    if not gid or gid not in GAMES:
        return redirect(url_for("index"))
    game = GAMES[gid]
    return render_template("game.html", game=game)


@app.route("/roll", methods=["POST"]) 
def roll():
    gid = session.get("game_id")
    if not gid or gid not in GAMES:
        return redirect(url_for("index"))
    game = GAMES[gid]
    player = game.players[game.current]

    # Play a turn for the current player
    result = game.play_turn(player)

    if not game.winner:
        game.next_player_index()

    return redirect(url_for("game_view"))


@app.route("/reset", methods=["POST"]) 
def reset():
    gid = session.get("game_id")
    if gid and gid in GAMES:
        del GAMES[gid]
    session.pop("game_id", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
