# Unverified strategies

Drafts whose timestamps have **not** been reproduced from `data/sc2_data.json`. Treat every timing here as a hypothesis.

To promote to `../verified/`: recompute each timestamp with the `sc2-timings` skill; fix anything impossible or off (production rate, tech chain, resources/supply under the 8-worker 5.0.16 economy); then move the file and record the patch it was verified against.
- `sc2_2v2_two_base_timing.html` — 2v2 P+T low-micro plan: no harass units, probe + Observer scouting, shared wall + Battery through the rush window, one synced Colossus/Chargelot + stim-bio punch at 8:30-9:00. Timings computed from the DB (post building-time fix); supply/resource gating are estimates until reproduced from a played replay.
- `sc2_protoss_double_robo_colossus.html` — 2v2 Protoss low-micro macro build (Dante): standard macro open, 6 Stalkers for early defense, first Robotics Facility makes Observer (~4:34) then Immortal (~5:13), double robo into Colossi (first ~6:40). The macro/defensive answer to the DT rush. Producer-start timings from the DB (patch 5.0.16); resource gating not yet reproduced.
- `sc2_protoss_oracle_expand.html` — 2v2 Protoss low-micro eco-tempo build (Dante): Stargate into Oracle (Stargate ~4:13, first Oracle ~4:50) for scouting + Pulsar Beam harass + defense, expand behind it. Branches into robo/Observer vs DT or Stargate/Void Rays into macro. Producer-start timings from the DB (patch 5.0.16); resource gating not yet reproduced.
