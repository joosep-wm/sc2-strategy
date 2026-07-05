# 2v2 Protoss + Terran — patch 5.0.16 research notes

**Status:** unverified (web research, 2026-07-05). §1 patch facts + §5 DT-rush timings ARE verified (release notes + `data/sc2_data.json`); §2–§4 strategy/resources are web-sourced and not DB-checked.
**Team:** Dante (Protoss, low-micro) + MadSysop (Terran). Format: 2v2 ladder.
**Repo rule:** timings come from the DB, not the web. Where a claim conflicts with the 5.0.16 **release** notes, the release notes win — the PTR notes had several values that were reverted (see §1).

---

## TL;DR — what to actually change

1. **Stop losing to early aggression by defending as a pair, not solo.** In 2v2 the attacker concentrates both armies on one defender; the standard loss is one of you getting picked off while the other macros obliviously. The single highest-value habit: **the moment either of you scouts aggression, both of you react** — pull the Terran's units/SCVs toward the threatened base, and use Protoss shared control to wall/block with the defender's buildings.
2. **The 5.0.16 economy rework is in your favor.** 8 starting workers (was 12) + reduced town-hall supply make early all-ins *more expensive and slower*. This is the strongest patch for a macro / 2-base-timing player in years. Your instinct (defend the rush window, then hit a 2-base timing) is exactly right for the meta — you just have to survive the first ~4 minutes.
3. **Your old build-order muscle memory is stale.** Every pre-2026 build assumes 12 workers. First pylon/supply depot, first gas, and every tech timing land *later* now. Don't copy 2013–2021 guides literally.

---

## 1. What patch 5.0.16 actually changed (22 Jun 2026, + 30 Jun hotfix)

Economy rework — the headline (verified across Blizzard notes + 3 analyses):
- **Starting workers 12 → 8.** Slows saturation and first expansion. Every early timing is pushed back.
- Large mineral patches **1,800 → 1,600**; small patches **900 → 1,100**; geysers **2,250 → 2,500** (gas/base 4,500 → 5,000). Net: flatter, longer economy curve; less "explosive" fast-tech off high-yield gas.
- **Town-hall supply cut 15 → 13** (Nexus, Command Center; Zerg Hatch line 6 → 4, cost up). You hit supply blocks sooner — build supply earlier than old habit says.

Protoss (matters for Dante) — **verified against the 5.0.16 RELEASE notes** (news.blizzard.com/24259080), not the PTR:
- **Warp Gate research still sits on the Cybernetics Core (50/50, 100f) — it did NOT move.** The PTR proposal to move it to the Gateway and cost 35%/50-50 was *reverted before release*. Ignore any guide citing "research on Gateway", "35%", "50/50 transform", or "3s warp-in" — those are dead PTR values.
- **Transforming a Gateway → Warp Gate now costs 25/25** (was free), **one-time per gate**; after buying you switch modes for free. So going warp-in is now a small economic commitment, not automatic.
- **Warpgate research speeds Gateway unit production ~40%.** Producing from a researched-but-*untransformed* Gateway is a legitimate lower-micro option (rally units out, no warp-in decisions).
- **Warp-in time = 4 seconds** (release notes; was "3.6s / 11.4s slow-field"). HT/DT warpgate cooldown 35 (slightly longer gap than basic units).
- Psi Storm damage 110 → 100 (minor; you're low-micro so storm isn't your core anyway).

Terran (matters for MadSysop):
- **Ghost buffed but pricier:** supply 2 → 3, HP 125 → 100, attack 15 (was 10+10 vs light), range 6 → 7. Stronger generalist / anti-caster, more fragile.
- Command Center supply 15 → 13 (as above).

Zerg (what you'll face): faster larva (10.7 → 9.5s), stronger Infestor (Microbial Shroud range 9 → 12, no upgrade needed), Baneling splash now hits allied units too.

**30 Jun hotfix:** Force Field adjustment among small tweaks — check current notes before a tournament, but nothing that changes the strategic picture below.

**Meta verdict (consistent across all sources): early cheese/all-ins are weaker, macro is stronger.** "Early game pressure has become more expensive." This is the patch to be a macro player.

---

## 2. 2v2 strategy for Protoss + Terran

### 2v2 is a different game from 1v1 — the three rules
1. **Two armies focus one target.** Whoever gets attacked must survive until the partner arrives. Defense is a *team* action, not a solo one.
2. **Information wins.** Hold the Xel'Naga watchtowers (map vision) — Liquipedia's top general-2v2 advice is "emphasize information over brute warfare." You lose to what you don't scout.
3. **Shared mechanics are tools, not decoration:**
   - **Shared control** (on by default) — your partner can move your units/SCVs to help wall a ramp, pull workers, or block a runby. Some pros disable it mid-fight to keep clean micro; for you, leave it on for defense.
   - **Shared resources** unlock at **5:00** — a stabilizing partner can float minerals/gas to the attacked player, or fund a surprise timing.

### The Protoss+Terran combo — why it's strong, and the current-patch version
The classic synergy (still true): **Terran ranged core + Protoss front-line and utility.** Concretely:
- **Protoss provides the wall and the shields:** Zealots/Sentries (Guardian Shield cuts ranged damage) tank in front of Terran Marines/Marauders. Immortals eat armored (tanks, roaches).
- **Terran provides ranged DPS and detection:** Marauders vs armored, Marines vs light/air, scans for cloak, tanks for zone control.
- **Air:** Protoss Stargate (Phoenix/Void Ray) + Terran Vikings/Banshees is a flexible air package; Phoenix lift + Terran ground is a strong pick combo.

> ⚠️ **Stale-source warning:** The most-linked "Terran+Protoss 2v2" web guide (osirissc2guide.com) is **Heart of the Swarm era (~2013–2014)** — its exact builds (12-worker starts, 9-pylon/10-gate, 7-rax proxy reaper) are obsolete on 5.0.16. Keep the *combo logic* above; ignore its numbers.

### Defending the early rush window (your #1 leak)
The 2v2 games you lose are almost all decided in the first 4 minutes. Plan for these:
- **Proxy / 2-base all-in on one player:** the scouted-on player calls it *immediately*; both pull toward that base. Protoss holds a ramp with Zealot + Sentry force-field (FF got a hotfix buff — useful); Terran adds a Bunker + SCV repair. A bunker with 2–4 marines behind a partial wall stops most early ground pushes.
- **Cannon / Bunker rush in your base:** pull ~4–6 workers onto the builder immediately; a proxy building dies fast to focused worker fire if you react in the first 10 seconds. Don't let it finish.
- **Air cheese (Oracle / Banshee / Void):** this is why detection + a stargate/turret matters early. Terran scan or a Photon/Turret at each mineral line. One of you should have anti-air online by ~3:30.

**Because of 5.0.16, all of these arrive later and with fewer units than the old guides assume** — you have more margin than pre-patch. Use it: scout, react together, then macro.

### Your game plan (fits low-micro Protoss + Terran)
1. **Both open economic-but-safe** — no greedy fast-expand into an un-scouted 2v2, but no all-in either. Build supply early (town halls give less now).
2. **One of you takes map vision** (watchtowers) and calls threats.
3. **Survive to ~5:00**, when shared resources unlock and your 2-base economy comes online.
4. **Hit a 2-base timing together** — Protoss Immortal/Zealot/Sentry + Terran Marauder/Marine/Tank is a forgiving, low-micro, high-value push. Concentrate on one opponent; ignore expansions until a base is dead (kill one player → 2v1).

---

## 3. Protoss builds for a low-micro macro player (current patch)

The macro spine (unchanged in structure): **Gateway → Assimilator → Nexus → Cybernetics Core → (first tech) → Warp Gate.** First-tech fork:

- **Robotics-first = the low-micro default.** Observer gives you detection + scouting for free (no micro), Immortals are point-and-click vs armored, and it covers most ground threats. Best fit for "defend the rush window then 2-base timing."
- **Stargate (Oracle/Phoenix)** is stronger but wants more micro — Oracle harass and Phoenix lifts reward APM you've said you don't want to spend. In 2v2, a *defensive* stargate (a couple of Void Rays / a Phoenix for detection + air D) is fine; skip the harass game.

**Current-patch note:** with the warpgate rework, **you can produce from researched-but-untransformed Gateways** (faster than before) instead of committing to warp-in. That's a legitimately lower-micro macro option now — fewer warp-in decisions, just rally units out. Try it.

> ⚠️ Do **not** trust exact supply/timing numbers from web build guides on this patch — they're mostly pre-2026. Reproduce any opener against `data/sc2_data.json` before you rely on it. That's what the repo's `sc2-timings` skill is for.

---

## 4. Learning resources (current as of mid-2026)

**2v2-specific (rare — most content is 1v1 that transfers):**
- **Liquipedia — [General 2v2 strategy](https://liquipedia.net/starcraft2/General_2v2_strategy)** — patch-agnostic, still the best free 2v2 primer (watchtowers, shared control/resources, race-pairing notes; T/Z rated strongest overall).
- ⚠️ **osirissc2guide.com Terran+Protoss 2v2** — combo logic OK, builds are HotS-era. Reference for *ideas*, not numbers.

**Build-order databases (keep these current):**
- **[Spawning Tool](https://lotv.spawningtool.com/build/)** — the standard build-order DB with replay examples; filter by matchup ([PvX](https://lotv.spawningtool.com/build/pvx/), [TvX](https://lotv.spawningtool.com/build/tvx/)). Check upload dates — grab post-Jun-2026 builds.
- **[Liquipedia](https://liquipedia.net/starcraft2/)** — unit stats, tech, patch history (your DB's primary source).

**YouTube / coaching (1v1 fundamentals that transfer to 2v2):**
- **PiG — Bronze-to-GM (B2GM)** — the standard structured ladder-improvement series; best single resource for macro hygiene (don't get supply-blocked, keep producing). Watch for his 5.0.16-updated content.
- **LowkoTV, WinterStarcraft, uThermal** — casts/coaching content; good for absorbing decision-making.
- **Coaches:** Jumy (pro Protoss, Germany), VoidRay (NA/EU Protoss) — via learningsc2.com if you want paid Protoss-specific review.

**Tools:**
- **AI replay analysis** (e.g. starcraft2.ai) — upload a `.SC2Replay`, get economy/build-execution feedback. Useful, but treat its patch claims skeptically and cross-check against your DB.
- **Your own repo** — the `sc2-timings` skill + `sc2_data.json` is your ground truth for 5.0.16 numbers. **This is more current and more reliable than any web build guide for exact timings.**

---

## 5. Anti-DT-rush: the loss on 2026-07-05 (DB-verified timings)

**What happened:** enemy Protoss proxy-pylon DT all-in. ~4 warpgates, 3 DTs at Dante's base at **~5:00**. Dante killed a few of the enemy's probes at his base and it changed nothing.

**Is the story physically real? Yes.** DB tech chain to the first DT:
`Nexus → Gateway (46f) → Cybernetics Core (36f) → Twilight Council (36f) → Dark Shrine (71f)` — prereq buildings that must exist = **118f** on top of the starting Nexus, and they overlap (probe walks + build in parallel). To *warp* DTs he also needs **Warpgate research (100f)** running concurrently. On a committed one-base proxy DT all-in, **Dark Shrine + Warpgate research both finishing ~4:40–5:00 is achievable**, and then **all warpgates warp simultaneously** — 4 warpgates = **4 DTs on the map in a 4-second warp-in** (warp-in time = 4s, verified). Pre-placed proxy pylon = they appear *in your base*, not walking from his. 3 DTs at 5:00 is a textbook execution, not a misremember.

**Why killing his probes did nothing:** a DT all-in *sacrifices economy on purpose.* His probe count was irrelevant to him — he spent everything on tech + warp gates and was never going to macro. Trading in his base fought the all-in **on his terms.** The only thing that beats it is **detection + defenders at home before 5:00.**

### The hard rule this loss teaches
**DTs are invisible. Colossi, Immortals, Stalkers — none of them can shoot what you can't see.** Static army does nothing without a detector. The counter is *seeing* them, then having *anything* that shoots.

### Detection options and when they're ready (DB, faster clock)
| Source | Needs | First detection online | Note |
|---|---|---|---|
| **Observer** | Robotics Facility | Robo start 3:30 → Obs pops **4:34** | Best fit for a robo player — it's already on your path. Mobile, cloaked. |
| **Photon Cannon** | Forge (36f) → Cannon (29f) | Forge+Cannon started ~4:00 → done **~4:35+** | Static; also *shoots* DTs. Put one at each mineral line. |
| **Terran partner's Scan** | Orbital Command | On demand from ~3:30+ | In 2v2 this is huge — MadSysop scans your base the instant DTs land, your army does the rest. Free detection you already have. |

### Your double-robo Colossus plan — the one correction
Cranking 3–4 Colossi is a fine *game plan* and a great low-micro army. But against this specific rush it has a **timing trap**:

- First **Colossus pops ~6:40** (Robo 46f → Robo Bay 46f → Colossus 54f is a long chain). **That is 1:40 too late** — the DTs arrive at 5:00 and the game is decided before your first Colossus exists.
- **The Robo's job in the first 5 minutes is an OBSERVER (pops 4:34), not a Colossus.** Same building, and the Observer is *ahead* of the DTs. Build Obs first, *then* Robo Bay + Colossi.
- Faster killing power if you scout DT tech: **Immortal pops ~5:25 from a Robo starting at 4:00** — point-and-click, no micro, shreds anything that stands still. Two Immortals + an Observer is a clean, low-micro DT answer.

### Dante's standing robo rule (2026-07-05)
**First robo always makes an Observer, then an Immortal. When the robo finishes, start a Robotics Bay + a 2nd Robo.** DB-verified timings (robo starting ~3:30):

| Unit / building | Pops / done | vs the 5:00 DT rush |
|---|---|---|
| Observer (1st from robo) | **~4:34** | ✅ detection *before* the DTs |
| Immortal (2nd from robo) | **~5:13** | ⚠️ lands as/just after DTs — once they're revealed, Immortal barrier shreds them |
| Robotics Bay + 2nd Robo | start when robo done (~4:16), 46f each | macro/Colossus tech comes online ~6:30+ |

This is the right **default** — one rule, no scouting-dependent decisions, closes the DT hole every game. **The tradeoff:** Obs-first pushes the Immortal ~40s later than Immortal-first, so the 4:34→5:13 window is thin. **The insurance for a *fast* all-in:** MadSysop's **Scan** the instant DTs land + a couple of Stalkers or a Cannon to bridge that gap. Default = this rule; insurance = the Scan.

### Anti-DT checklist (do this every game until it's automatic)
1. **Scout the enemy Protoss by ~2:30–3:00.** A fast Twilight Council / Dark Shrine, few units, and missing expansion = DT or all-in tech. Missing army is the tell.
2. **Have detection at home by 4:30**, not 5:30. Observer (robo) or Cannon (forge) or partner Scan — pick one and commit.
3. **Have SOMETHING that shoots by 5:00** near your mineral lines and Nexus — 2 Immortals, or Stalkers, or Cannons. DTs die fast once revealed.
4. **In 2v2, call it the second you scout it** — MadSysop pre-positions a scan + a few Marines/Marauders at your base. Two players covering one base beats 4 DTs easily.
5. **Don't chase his workers.** His economy is already spent. Defend, hold, then his all-in is a dead-end and you win the macro game the patch already tilts your way.

> ✅ **Timings in this section are reproduced from `data/sc2_data.json` (patch 5.0.16).** Detection/army pop times assume the producer starts at the stated time and ignore resource gating + travel — treat as "earliest realistic," verify the exact opener when you build it. Warp-in time (4s), transform cost (25/25 one-time), and 40% Gateway speedup are from the 5.0.16 release notes.

---

## Sources
- [Blizzard 5.0.16 patch notes](https://news.blizzard.com/en-us/article/24259080/starcraft-ii-5-0-16-patch-notes)
- [vpesports — 5.0.16 new economy analysis](https://vpesports.com/featured-news/starcraft-2-patch-new-economy)
- [strafe.com — 5.0.16 economy + warpgate breakdown](https://www.strafe.com/news/read/star-craft-ii-patch-5-0-16-ptr-economy-protoss-warpgate-and-balance-changes/)
- [starcraft2.ai — 5.0.16 what changed](https://www.starcraft2.ai/en/guides/sc2-patch-5016)
- [Liquipedia — General 2v2 strategy](https://liquipedia.net/starcraft2/General_2v2_strategy)
- [osirissc2guide — Terran/Protoss 2v2 (⚠️ HotS-era, dated)](https://osirissc2guide.com/starcraft-2-terran-protoss-2v2-strategies.html)
- [Spawning Tool build DB](https://lotv.spawningtool.com/build/)

## Resolved this session (2026-07-05)
- ✅ Warp-in time = **4s**, transform cost = **25/25 one-time**, Gateway speedup = **40%**, research **stays on Cyber Core** — verified against 5.0.16 release notes. PTR values (3s / 50-50 / 35% / research-on-Gateway) were reverted; discard.
- ✅ DT-rush timing (§5): 3–4 DTs at ~5:00 from a proxy DT all-in is real. Counter = detection by 4:30 (Observer 4:34 / Cannon / partner Scan) + something that shoots by 5:00 (Immortal 5:25). First Colossus (~6:40) is too late to defend it — robo makes an **Observer first**.

## Open items to verify against the DB before promoting to verified/
- A concrete 5.0.16 robo-first 2-base timing opener, supply-by-supply, reproduced from `sc2_data.json` (the §5 pop times assume producer-start times; a full opener needs resource gating).
- Whether "produce from untransformed Gateway" (~40% faster) beats warp-in for your specific unit mix (compute from DB).
