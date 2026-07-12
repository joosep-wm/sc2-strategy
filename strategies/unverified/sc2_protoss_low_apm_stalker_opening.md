# Low-APM Safe Opening: Continuous Stalker + Natural Battery

Status: unverified draft (repo convention). Patch 5.0.16, Faster clock. Every timing below is either an anchor observed in the repo's verified Stargate opening replay or computed from sc2_data.json build times. Sources noted per line.

## Why this replaces the double-Adept opening for Kaido

Replay evidence (60 games, 2026-07):
- First gateway unit born at median 3:12; enemy first kills in our base start at 2:49.
- Only 2 combat units by 4:00, 3 to 4 by 5:00.
- Early-harassed games: 25% winrate, 12 workers lost on average before 7:00.
- Double-Adept shade micro exceeds available APM and pulls focus from probes and pylons (self-reported, consistent with the 30 to 210s supply blocks in replays).

Design goals: first defender out before the earliest observed harass; a unit every 27s with zero micro; Battery at the natural as standard; one decision point, one tech path.

## Feasibility check (DB)

- Stalker: 125m 50g, 27s build (sc2db). One gate nonstop needs ~111 gas/min.
- One geyser, 3 workers: ~114 gas/min (DB mining model). Gas #1 alone funds continuous Stalkers.
- Shield Battery: 100m 0g, 29s, requires only a Gateway (sc2db).
- Minerals are not the constraint: historical mid-game banks were 600+.

## Build order

Anchors from the verified opening are marked (v); DB-computed times marked (db).

| Supply | Time | Action |
|---|---|---|
| 11 | ~0:25 | Pylon (v) |
| 12 | 0:47 | Gateway, done 1:34 (v) |
| 13 | ~0:55 | Assimilator, 3 probes in gas immediately |
| 15 | ~1:30 | Pylon |
| 17 | 1:42 | Cybernetics Core, done 2:18 (v) |
| 20 | 2:18 | Stalker #1, born 2:45 (db: 27s). Hold at your mineral line |
| 22 | 2:45 | Stalker #2, born 3:12 (db). Gate never idles from here on |
| 22 | ~2:45 | Probe scout leaves to check the enemy natural (see scout rule) |
| 24 | ~3:12 | Nexus at the natural (v anchor) |
| 24 | ~3:20 | Shield Battery at the natural, done ~3:49 (db: 29s). Cover the nat mineral line and the choke |
| 26 | ~3:30 | Assimilator #2 (funds the tech path, not the Stalkers) |
| 28 | ~3:45 | Gateway #2 |
| 30 | ~4:00 | Pylon; keep Stalkers flowing: born 3:39, 4:06, 4:33, 5:00 (db cadence) |
| ~36 | ~4:30 | Warp Gate research (50/50, 100s, db) |
| ~45 | 5:30 | Decision point: pick ONE tech path |

Result at 5:00: 6 Stalkers, Battery, two bases, two gates. Previous reality at 5:00: 3 to 4 units, no Battery.

## Rules

- Chrono: probes only until 5:30 (verified build rule, unchanged).
- The gate is never idle. If gas dips (you built the Battery late or lost probes), insert a Zealot (100m 0g, 27s) instead of waiting.
- Low-APM Warp Gate option (DB note): after Warp Gate research completes, an untransformed Gateway produces about 40% faster. You get most of the benefit with zero warp-in micro. Transform (25m 25g each, 5.0.16 cost) only when you actively want warp-ins at a forward pylon.
- Scout rule (from 66 opponents measured): enemy natural starts at median 3:06. If your probe sees NO enemy natural by 3:30: second Battery immediately, Stalkers from both gates, no tech until 6:00. Observed one-base all-ins ended games at 4:57 to 6:02.
- No second tech building before the 5:30 decision, ever. Tech sprawl was the number one loss pattern in the 2v2 set.

## The four tech paths at 5:30 (unchanged preferences, one per game)

1. Robo into Colossus: use the repo draft sc2_protoss_double_robo_colossus with its known fix (start Robo on time so the Observer is out before the DT window).
2. Twilight into Zealot/Templar/Archon: Storm is 100 damage in 5.0.16 (was 110); Charge zealots and Archons are the lowest-micro late army of the four.
3. Dark Shrine: DT pressure works only if it is the ONLY tech; the replays show late panic Dark Shrines (minute 14+) never work.
4. Stargate into Fleet Beacon and Mothership: most expensive path; only when scouted safe on both fronts in 2v2.

## What changes vs the verified Stargate opening

Removed: Adept pair and their shade micro, early Oracle. Cost: less scouting information and no early worker kills. Compensation: dedicated probe scout at 2:45 plus the 3:30 rule. Added: Stalker at 2:45 (before earliest observed harass at 2:49), continuous production, standard natural Battery at ~3:49.

## Verification status

Not yet flown in a game. Promotion to verified per repo rules requires reproducing each timestamp in a replay. Suggested test: 3 games vs AI or unranked, check: Stalker #1 born by 2:50, Nexus by 3:15, Battery done by 3:55, 6 Stalkers at 5:00, zero gate idle time.
