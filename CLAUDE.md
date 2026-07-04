# CLAUDE.md — SC2 strategy repo

Purpose: design StarCraft II strategies (single-file HTML guides) whose timings are grounded in a verified, current-patch data set — not vibes.

## Layout

```
data/
  sc2_data.json          ground-truth DB: costs, supply, build/research times, tech, economy. Patch 5.0.16.
  README.md              DB documentation + conventions
strategies/
  unverified/            drafts; timings not yet checked against the DB
  verified/              timings reproduced from the DB (records the patch verified against)
.claude/skills/sc2-timings/   repo skill for querying the DB and computing/validating timings
```

## Rules

- **Any SC2 timing/cost/tech claim must come from `data/sc2_data.json`, not memory.** Use the `sc2-timings` skill (it has a query tool). The DB is the single source of truth.
- **Always plan in `*_faster` seconds** (the in-game Faster clock = build-order mm:ss). `*_normal` is raw data only; `faster = normal / 1.399902`. Getting this backwards is the #1 error — the DB `meta.time_convention` has the anchors.
- New/draft strategies go in `strategies/unverified/`. Only move to `strategies/verified/` after every timestamp is reproducible from the DB (see the skill's promotion rule). Verified strategies note the patch.
- Current patch is **5.0.16** (starting workers 8, not 12). If a newer patch is live, update the DB first (Liquipedia + official notes), preserving the faster/normal normalization.
- Follow global style prefs: concise, code over prose, smallest correct change, no needless comments.

## Common tasks

- Look up a value / tech chain → `sc2-timings` skill → `sc2db.py find|get|tech`.
- "When does X pop / is this timestamp real?" → skill → `sc2db.py pop` + resource/supply gating from `sc2db.py constants`.
- Revise a strategy → validate against DB, correct the timeline, then promote unverified→verified.
