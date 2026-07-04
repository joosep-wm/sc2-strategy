# SC2 Ground-Truth Timings DB

`sc2_data.json` — costs, supply, build/research times, tech tree, and economy model for **StarCraft II patch 5.0.16** (22 Jun 2026, Blizzard economy rework). Built from Liquipedia stat pages + the official 5.0.16 notes, cross-checked and normalized. Use it to compute and validate build-order timings.

## The one thing that trips everyone up: time units

Build/research times are stored in **Normal** game-seconds but the game **displays real-time**, and on **Faster** (ladder standard) the in-game clock itself runs in real-time.

```
faster_s = normal_s / 1.399902   (~ /1.4)
```

- **`*_faster` = what the in-game clock shows = what build orders (mm:ss) use.** Plan with this.
- **`*_normal` = raw data value.** Reference only.
- Anchors: Marine 25n/18f · SCV 17n/12f · Command Center 71n/51f · Zealot 38n/27f.
- ⚠️ Liquipedia is inconsistent (Unit Statistics page = Faster, Building Statistics page = Normal). Everything in the JSON is already normalized so `*_faster` is always real-time.

## Structure

```
meta        patch, sources, field glossary, time convention, provenance/verify flags
constants   start (8 workers!), 5.0.16 resources, mining model, macro mechanics
units       {Terran,Protoss,Zerg}[]  mins gas supply bt_faster bt_normal from req morph_from hp shield armor attributes
buildings   {Terran,Protoss,Zerg}[]  mins gas bt_normal bt_faster from req provides_supply hp
upgrades    {Terran,Protoss,Zerg}[]  mins gas rt_faster rt_normal at req effect
benchmarks  empirical mm:ss reference build orders (for cross-checking; travel-dependent)
```

## Computing a build-order timing (Faster clock)

An item completes at `start_time + bt_faster`. Chain prerequisites and gate on resources/supply.

Example — proxy Barracks first Marine:
`SCV leaves ~0:25 → travels 60-70% map → Barracks starts ~1:05, done +33s ≈ 1:38 → Marine +18s ≈ 1:56 → walks to enemy ≈ 2:05.` (Matches the benchmark.)

Chrono Boost / Warp Gate: multiply the affected `bt_faster` (Chrono = ×2/3 while active; Warp Gate produces Gateway units ~40% faster).

## 5.0.16 gotchas that change old guides

- **Starting workers 12 → 8.** Every economy/early timing from pre-2026 guides is now slower — the biggest reason to re-time old builds.
- Town-hall supply cut: CC/Nexus 15→13, Hatchery 6→4. Start supply is 8/13 (T,P) and 8/12 (Z), so first Depot/Pylon/Overlord is needed sooner.
- Warp Gate transform now costs 25/25 per gate (was free). Hatchery 275→300. Psi Storm 110→100 dmg. Zerg Carapace cheaper. Larva timer 10.7→9.5s (faster).

## Sources & audit

Liquipedia (Unit/Building Statistics LotV, upgrade pages), Blizzard 5.0.16 patch notes (`article/24259080`), Liquipedia Patches. Raw multi-agent research dump: `scratchpad/tasks/wxr9np23v.output`. See `meta.verify_flags` for the few values worth re-checking for balance-precise work (per-unit combat reworks; worker mining rates are approximations).
