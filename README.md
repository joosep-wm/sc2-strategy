# sc2-strategy

StarCraft II strategy guides with timings grounded in a verified, current-patch data set.

## Layout

- **`data/`** — `sc2_data.json` ground-truth DB (patch 5.0.17) + `README.md` docs.
- **`strategies/sim/`** — simulator build files behind each strategy's timeline.
- **`strategies/unverified/`** — drafts; timings not yet checked against the DB.
- **`strategies/verified/`** — timings reproduced from the DB.
- **`.claude/skills/sc2-timings/`** — skill + query tool for using the DB.

## Using the data

```
python3 .claude/skills/sc2-timings/scripts/sc2db.py find marine
python3 .claude/skills/sc2-timings/scripts/sc2db.py pop "Marine" 1:05
python3 .claude/skills/sc2-timings/scripts/sc2db.py constants
python3 .claude/skills/sc2-timings/scripts/sim.py strategies/sim/three_nexus_chargelot.txt
```

Plan in `*_faster` seconds (the in-game Faster clock = build-order mm:ss). See `data/README.md` for the full convention and `CLAUDE.md` for repo rules.
