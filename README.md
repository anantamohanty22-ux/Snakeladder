# Snake and Ladder (CLI)

Simple Python implementation of Snake and Ladder with a command-line runner.

Run:

```bash
python run_game.py
```

Features:
- Two to six players
- Human or AI players
- Classic snakes and ladders mapping
- Exact roll required to land on 100

Files:
- `src/snake_ladder.py` - core game logic
- `run_game.py` - CLI runner

Web frontend (two-player)
-------------------------
A simple Flask web frontend is provided at `src/web_app.py` for playing only two players (human vs human or human vs AI).

Install dependencies and run:

```powershell
py -m pip install -r requirements.txt
py src\web_app.py
```

Then open http://127.0.0.1:5000 in your browser.
