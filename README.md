# DomAIno

This is an environment to develop and test bots in the [Game of Dominoes](https://en.wikipedia.org/wiki/Dominoes).

## Quick reference

Show all available players and rules

`./main.py info`

Run a single match between `Big Drop` player and `Random` player.

`./main.py play --player0 BigDrop --player1 Random --rule OneGame`

After running the match you should see in the shell similar logs to:

```
NEW_GAME: []
MOVE: [0, (6, 5), 0]
MOVE: [1, (6, 4), 0]
MOVE: [2, (4, 3), 0]
MOVE: [3, (5, 4), 1]
MOVE: [0, (6, 3), 0]
MOVE: [1, (4, 2), 1]
MOVE: [2, (6, 2), 1]
MOVE: [3, (6, 6), 1]
PASS: [0]
PASS: [1]
MOVE: [2, (6, 1), 0]
MOVE: [3, (3, 1), 0]
MOVE: [0, (5, 3), 0]
MOVE: [1, (5, 5), 0]
MOVE: [2, (5, 1), 0]
MOVE: [3, (1, 1), 0]
MOVE: [0, (2, 1), 0]
MOVE: [1, (3, 2), 0]
MOVE: [2, (6, 0), 1]
MOVE: [3, (0, 0), 1]
MOVE: [0, (5, 0), 1]
MOVE: [1, (3, 0), 0]
MOVE: [2, (4, 0), 0]
MOVE: [3, (4, 4), 0]
MOVE: [0, (5, 2), 1]
MOVE: [1, (2, 2), 1]
MOVE: [2, (4, 1), 0]
FINAL: [2]
WIN: [0]
```

### Legend

+ `NEW_GAME []`: A new domino game started.
+ `MOVE [p, (v0, v1), h]`: Player `p` put piece `(v0, v1)` in head `h`
+ `PASS [p]`: Player `p` can't play.
+ `FINAL [p]`: Player `p` has not more pieces.
+ `WIN [t]`: Team `w` win. (-1 for ties)

## Add a new player

1. Create a class that inherit from [BasePlayer](player.py) (in [player.py](player.py)).
2. Register your player in [players/__init__.py](players/__init__.py) in the `PLAYERS` array.

Check already implemented [players](players/simple.py) as example.

## TODO List

+ Documentation
+ Allow human player (human teams)
+ UX
