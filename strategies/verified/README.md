# Verified strategies

Every timestamp here is reproducible from `data/sc2_data.json` (or explicitly annotated as an empirical/travel-dependent estimate). Each strategy notes the **patch** it was verified against — re-verify if the DB patch changes.

- `sc2_2v2_proxy_timing_build.html` — 2v2 Terran+Protoss proxy Rax/Gate into 2-base timing. Opening re-verified against patch **5.0.17** on 2026-10-21 with `strategies/sim/proxy_2v2_*.txt` (25s proxy walk assumed); proxy hit times annotated as travel-dependent estimates; the 2-base windows are shifted, not simulated.
- `sc2_protoss_stargate_opening.html` — Protoss double-gate Adept pressure → expand → Oracle, supply-driven, decision tree at 5:30. ⚠️ Verified against patch **5.0.16** only; not re-timed for 5.0.17, so treat it as unverified until it is. every timestamp observed in the source replay (`replays/2026-07-04_blackrock-le_pvp_dante-vs-edge.SC2Replay`) and cross-checked against the DB; harass hit times annotated as empirical.
