---
name: sc2-timings
description: Use when computing, validating, or revising StarCraft II build-order or strategy timings in this repo. Reads the ground-truth DB at data/sc2_data.json (patch 5.0.16) — unit/building/upgrade costs, supply, tech prerequisites, build times, and the economy model. Invoke for any question about SC2 timings, costs, tech trees, "when does X pop", whether a strategy's timestamps are realistic, or promoting a strategy from unverified to verified.
---

# SC2 timings skill

Ground-truth data lives in `data/sc2_data.json` (patch **5.0.16**). Never answer SC2 timing/cost questions from memory — query the DB. If a number isn't in the DB, look it up on Liquipedia and consider adding it (keep the convention below).

## The one rule you must never get wrong: time units

Times exist in two units. The DB stores both; **always plan with `*_faster`.**

- `*_faster` = **in-game clock (Faster) seconds** = what build orders (mm:ss) and the game UI show. **This is the planning unit.**
- `*_normal` = raw data (Normal) seconds. Reference only. `faster = normal / 1.399902`.
- Anchors to sanity-check any new number: Marine 25n/18f · SCV 17n/12f · Command Center 100n/71f · Zealot 38n/27f.
- Liquipedia is inconsistent (its Unit page shows Faster, its Building page shows Normal). The DB is already normalized; keep it that way if you add entries.

## Query tool

`python3 .claude/skills/sc2-timings/scripts/sc2db.py <cmd>` (works from any cwd; no deps):

| command | use |
|---|---|
| `find <query>` | fuzzy search across units/buildings/upgrades |
| `get "<exact name>"` | full entry + note/effect |
| `tech "<name>"` | producer + recursive prerequisite chain, with build times and a prerequisite-buildings total |
| `list <race> <units\|buildings\|upgrades>` | dump a category |
| `pop "<unit>" <mm:ss> [count]` | when unit(s) pop if its producer STARTS building at mm:ss (one at a time; pass count for N units) |
| `convert <sec> <faster\|normal>` | time conversion (the mode names the INPUT unit) |
| `constants` | economy model (starting workers, resources, mining, macro mechanics) |

For anything the tool doesn't cover, read `data/sc2_data.json` directly (it's structured and small).

## Computing a build-order timing (Faster clock)

1. An item completes at `start + bt_faster` (or `rt_faster` for upgrades). Chain prerequisites via `tech`.
2. **Production rate matters.** One structure makes one unit at a time: N units from one Barracks = first at `done+18f`, then `+18f` each. Don't assume a whole army pops at once. (Reactor = 2 at once for basic units; Warp Gate ≈ 40% faster Gateway units; Chrono Boost = ×2/3 while active.)
3. **Gate on resources & supply.** Use `constants`: **8 starting workers** (5.0.16), income model, and supply from town halls (13 T/P, Hatch 4) + Depot/Pylon/Overlord (8). A step can't start before you can afford it.
4. Travel/proxy: `pop` gives when a unit is *made*; add walk time for "reaches enemy". Proxies placed 60–70% across map → first proxy Marine hits ~2:00–2:15, first Zealot ~2:10–2:30 (see `benchmarks` in the DB).
5. Cross-check the result against `benchmarks` in the DB.

## Validating / revising a strategy

1. Read the strategy in `strategies/unverified/`.
2. Extract every claimed timestamp and army/production claim.
3. Recompute each from the DB (steps above). Flag any that are impossible or off (common failure: assuming multiple units from one production building appear simultaneously; using pre-2026 timings that predate the 8-worker economy).
4. Produce a corrected timeline with the reasoning (cite DB values).
5. **Promotion rule:** a strategy moves `unverified/ → verified/` only when every timestamp is reproducible from the DB (or explicitly annotated as an empirical/travel-dependent estimate). Note the patch it was verified against.

## When the patch changes

The DB is patch **5.0.16**. If a newer patch is live, re-verify affected numbers against Liquipedia + the official notes, update `data/sc2_data.json` and its `meta.patch`, and keep the faster/normal normalization.
