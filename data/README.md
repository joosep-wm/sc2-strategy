# SC2 Ground-Truth Timings DB

`sc2_data.json` — costs, supply, build/research times, tech tree, and economy model for **StarCraft II patch 5.0.17** (build 98310, live 8 Oct 2026 in EU), which rolled most of 5.0.16 back to 5.0.15. Built from Liquipedia stat pages and the official patch notes, cross-checked against Dante's 5.0.17 replays and normalized. Use it to compute and validate build-order timings.

## The one thing that trips everyone up: time units

Build/research times are stored in **Normal** game-seconds but the game **displays real-time**, and on **Faster** (ladder standard) the in-game clock itself runs in real-time.

```
faster_s = normal_s / 1.399902   (~ /1.4)
```

- **`*_faster` = what the in-game clock shows = what build orders (mm:ss) use.** Plan with this.
- **`*_normal` = raw data value.** Reference only.
- Anchors: Marine 25n/18f · SCV 17n/12f · Command Center 100n/71f · Zealot 38n/27f.
- ⚠️ Liquipedia is inconsistent (Unit Statistics page = Faster, Building Statistics page = Normal). Everything in the JSON is already normalized so `*_faster` is always real-time.

## Structure

```
meta        patch, sources, field glossary, time convention, provenance/verify flags
constants   start (12 workers), resources, replay-calibrated mining model, macro mechanics
units       {Terran,Protoss,Zerg}[]  mins gas supply bt_faster bt_normal from req morph_from hp shield armor attributes
buildings   {Terran,Protoss,Zerg}[]  mins gas bt_normal bt_faster from req provides_supply hp
upgrades    {Terran,Protoss,Zerg}[]  mins gas rt_faster rt_normal at req effect
benchmarks  empirical mm:ss reference build orders (for cross-checking; travel-dependent)
```

## Computing a build-order timing (Faster clock)

An item completes at `start_time + bt_faster`. Chain prerequisites and gate on resources/supply.

Example — proxy Barracks first Marine:
`SCV leaves ~0:25 → travels 60-70% map → Barracks starts ~1:05, done +46s ≈ 1:51 → Marine +18s ≈ 2:09 → walks to enemy ≈ 2:18.` (Benchmarks predate the 2026-07-05 building-time fix; re-verify before relying on them.)

Chrono Boost: +50% for 20s, so a boosted item finishes in 2/3 of its time while it lasts. Warp Gate: cycle = cooldown (Zealot/Adept 20s, Stalker/Sentry 23s, HT/DT 32s); warp-in 3.6s in a fast field runs inside it.

For whole builds use the simulator: `python3 .claude/skills/sc2-timings/scripts/sim.py strategies/sim/<build>.txt` (see the skill).

## 5.0.17 (8 Oct 2026): most of 5.0.16 is reverted

- **12 starting workers again**, Nexus/CC 15 supply, Hatchery 6 supply and 275 minerals. 12-worker-era guides (5.0.15 and earlier) are valid again for openings; anything timed on 8 workers is 20-40s late.
- **Warp Gate research no longer speeds up Gateways.** Transform is free, Warp Gates are the faster producer again, warp-in 3.6s fast field / 11.4s slow. Any build whose engine was the researched-Gateway Zealot (13.5s) has lost it.
- Economy 1800/900 patches, 2250 geysers. CC 400, PF 150/150. Adept 30s, +1(+1) per upgrade. Psi Storm 110. Colossus 10(+5). Larva 10.7s. Carapace 150/200/250.
- Unverified because the notes are silent: transform duration (kept 4s), HT/DT Gateway time (kept 40s from the 30 Jun hotfix), rich vespene (kept 6). See `meta.verify_flags`.

### Errors fixed on 2026-10-21 that predate 5.0.17

- The 30 Jun 2026 hotfix had never been applied (geyser 2000, larva 9.9, Reaper 34, Adept 33, HT/DT 40, Mothership 200/400). 5.0.17 reverted all of it except HT/DT 40.
- Chrono Boost lasts 20s Faster, not 14.3 (measured 19.9s in a replay).
- Gas was 114/min per geyser; replays show ~162. Minerals ~54 per worker-minute for the first 16 on a base (fitted to Emocan's 5.0.17 opener, within 1% at 2:09 and 4:00).

## Older: 5.0.16 / 5.0.16b gotchas (superseded)

- **Starting workers 12 → 8.** Every economy/early timing from pre-2026 guides is now slower — the biggest reason to re-time old builds.
- Town-hall supply cut: CC/Nexus 15→13, Hatchery 6→4. Start supply is 8/13 (T,P) and 8/12 (Z), so first Depot/Pylon/Overlord is needed sooner.
- Warp Gate transform now costs 25/25 per gate (was free). Hatchery 275→300. Psi Storm 110→100 dmg. Zerg Carapace cheaper. Larva timer 10.7→9.5s (faster).

### 5.0.16b hotfix (16 Jul 2026), applied 2026-09-20

- Warp Gate research train-time reduction **40% -> 50%**. A researched Gateway now builds Zealot 13.5f, Stalker 13.5f, Sentry 11.5f, Adept 15f, HT/DT 21.5f. Third-party guides still quoting 16/16/14/18 are on the pre-hotfix numbers.
- Gateway/Warp Gate transform duration **7s and 5s -> 4s** in both directions (cost still 25/25).
- Command Center **400 -> 300** minerals; Planetary Fortress **150/150 -> 250/150**; Ghost supply **3 -> 2**.
- Colossus damage **10(+5 vs Light) -> 12(+3 vs Light)**; Adept weapon-upgrade step **1(+1) -> 2(+2 vs Light)**; Disruptor phantom weapon range **11.35 -> 7**.

## Sources & audit

Blizzard 5.0.17 notes (`article/24309308`) and Liquipedia Patch 5.0.17, which agree line for line; Blizzard 5.0.16 (`article/24259080`), 30 Jun hotfix (`article/24289266`) and 5.0.16b (`article/24291949`) notes; Liquipedia stat pages (unit pages are stale, pre-5.0.14). Replay checks: Dante's 5.0.17 ladder 2v2 of 2026-10-20 and 84 replays since 2026-08-25 for mining. Raw multi-agent research dump: `scratchpad/tasks/wxr9np23v.output`. See `meta.verify_flags` for the few values worth re-checking for balance-precise work (per-unit combat reworks; worker mining rates are approximations).
