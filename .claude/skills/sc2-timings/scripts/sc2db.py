#!/usr/bin/env python3
"""Query helper for the SC2 ground-truth timings DB (data/sc2_data.json).

Times: *_faster = in-game clock (Faster) seconds — use these for build orders.
       *_normal = raw data (Normal) seconds. faster = normal / 1.399902.

Usage:
  sc2db.py find <query>                 fuzzy search units/buildings/upgrades
  sc2db.py get "<exact name>"           full entry (all races/categories)
  sc2db.py tech "<unit or building>"    producer + prerequisite chain + total
  sc2db.py list <race> <units|buildings|upgrades>
  sc2db.py pop "<unit>" <mm:ss> [count] when unit(s) pop if the producer STARTS at mm:ss
  sc2db.py convert <seconds> <faster|normal>   (names the INPUT unit)
  sc2db.py constants
Race is case-insensitive (terran/protoss/zerg). Errors exit nonzero.
"""
import json, os, sys

FASTER = 1.399902343750
TOWNHALLS = {"Nexus", "Command Center", "Hatchery"}

def die(msg):
    print(msg)
    sys.exit(1)

def find_db():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        p = os.path.join(d, "data", "sc2_data.json")
        if os.path.exists(p):
            return p
        d = os.path.dirname(d)
    die("ERROR: could not locate data/sc2_data.json above " + os.path.abspath(__file__))

def load():
    with open(find_db()) as f:
        return json.load(f)

def mmss(sec):
    sec = round(sec)
    return f"{sec // 60}:{sec % 60:02d}"

def parse_mmss(s):
    try:
        if ":" in s:
            m, sec = s.split(":")
            return int(m) * 60 + int(sec)
        return float(s)
    except ValueError:
        die(f"ERROR: '{s}' is not a valid time (use seconds or mm:ss)")

def all_entities(db):
    for cat in ("units", "buildings", "upgrades"):
        for race, arr in db[cat].items():
            for e in arr:
                yield cat, race, e

def fmt(cat, race, e):
    if cat == "units":
        t = f"{e['bt_faster']}f/{e['bt_normal']}n"
        return f"[{race} unit] {e['name']}: {e['mins']}m/{e['gas']}g sup{e['supply']} bt {t} from {e['from']} req {e.get('req',[])}"
    if cat == "buildings":
        t = f"{e['bt_faster']}f/{e['bt_normal']}n"
        sup = f" +{e['provides_supply']}sup" if e.get("provides_supply") else ""
        return f"[{race} building] {e['name']}: {e['mins']}m/{e['gas']}g bt {t}{sup} from {e['from']} req {e.get('req',[])}"
    t = f"{e['rt_faster']}f/{e['rt_normal']}n"
    return f"[{race} upgrade] {e['name']}: {e['mins']}m/{e['gas']}g rt {t} at {e['at']} req {e.get('req',[])}"

def lookup(db, name):
    """Exact match; falls back to Terran add-on aliases (e.g. 'Barracks Tech Lab' -> 'Tech Lab (add-on)')."""
    q = name.lower().strip()
    alts = {q}
    if q.endswith("tech lab"):
        alts.add("tech lab (add-on)")
    if q.endswith("reactor") and "(add-on)" not in q:
        alts.add("reactor (add-on)")
    for c, r, e in all_entities(db):
        if e["name"].lower() in alts:
            return c, r, e
    return None, None, None

def cmd_find(db, q):
    ql = q.lower()
    hits = [(c, r, e) for c, r, e in all_entities(db) if ql in e["name"].lower()]
    if not hits:
        die("no matches for " + q)
    for c, r, e in hits:
        print(fmt(c, r, e))

def cmd_get(db, name):
    c, r, e = lookup(db, name)
    if not e:
        die("not found (try `find`): " + name)
    print(fmt(c, r, e))
    if e.get("note"): print("  note:", e["note"])
    if e.get("effect"): print("  effect:", e["effect"])

def cmd_tech(db, name):
    c, r, e = lookup(db, name)
    if not e:
        die("not found: " + name)
    print(fmt(c, r, e))
    print("  produced from:", e.get("from", ""))
    chain, seen = {}, set()
    def walk(reqs, depth):
        for req in reqs:
            cc, _, re_ = lookup(db, req)
            bt = re_.get("bt_faster") if re_ else None
            disp = re_["name"] if re_ else req
            print("  " * depth + "- " + disp + (f" ({bt}f)" if bt is not None else ""))
            if re_ and req.lower() not in seen:
                seen.add(req.lower())
                if cc == "buildings":
                    chain[re_["name"]] = re_["bt_faster"]
                walk(re_.get("req", []), depth + 1)
    print("  prerequisites:")
    walk(e.get("req", []), 2)
    if chain:
        total = sum(chain.values())
        base = sum(v for k, v in chain.items() if k in TOWNHALLS)
        line = f"  prerequisite buildings bt_faster total: {int(total)}f"
        if base:
            line += f" (excl. pre-existing starting base: {int(total - base)}f)"
        print(line)
        print("  (add the direct producer's bt_faster + the unit's own bt_faster for time-to-first)")

def cmd_list(db, race, cat):
    race = race.capitalize()
    if cat not in ("units", "buildings", "upgrades"):
        die("category must be units|buildings|upgrades")
    arr = db.get(cat, {}).get(race)
    if arr is None:
        die(f"no {cat} for {race} (races: Terran, Protoss, Zerg)")
    for e in arr:
        print(fmt(cat, race, e))

def cmd_pop(db, unit, start, count="1"):
    c, r, e = lookup(db, unit)
    if c != "units":
        die("not a unit: " + unit)
    try:
        count = max(1, int(count))
    except ValueError:
        die("count must be an integer")
    t0 = parse_mmss(start)
    prod_name = e["from"].split(" / ")[0].split(" (")[0].strip()
    _, _, pb = lookup(db, prod_name)
    if not pb:
        die(f"{e['name']}: producer '{prod_name}' not found in buildings")
    struct_done = t0 + pb["bt_faster"]
    print(f"{r} {e['name']} via {pb['name']} (bt {pb['bt_faster']}f) + unit (bt {e['bt_faster']}f), one at a time")
    print(f"  producer starts {mmss(t0)} -> producer done {mmss(struct_done)}")
    for i in range(count):
        t = struct_done + (i + 1) * e["bt_faster"]
        print(f"  #{i+1} pops {mmss(t)}")
    print("  (ignores resource/supply gating and travel; assumes producer built from scratch at start)")

def cmd_convert(_, sec, mode):
    try:
        sec = float(sec)
    except ValueError:
        die(f"ERROR: '{sec}' is not a number")
    if mode == "faster":
        print(f"{sec} faster-s = {sec*FASTER:.1f} normal-s")
    elif mode == "normal":
        print(f"{sec} normal-s = {sec/FASTER:.1f} faster-s ({mmss(sec/FASTER)})")
    else:
        die("mode must be 'faster' or 'normal' (it names the INPUT unit)")

def cmd_constants(db):
    print(json.dumps(db["constants"], indent=2))

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    db = load()
    cmd, rest = a[0], a[1:]
    try:
        if cmd == "find": cmd_find(db, rest[0])
        elif cmd == "get": cmd_get(db, rest[0])
        elif cmd == "tech": cmd_tech(db, rest[0])
        elif cmd == "list": cmd_list(db, rest[0], rest[1])
        elif cmd == "pop": cmd_pop(db, rest[0], rest[1], rest[2] if len(rest) > 2 else "1")
        elif cmd == "convert": cmd_convert(db, rest[0], rest[1])
        elif cmd == "constants": cmd_constants(db)
        else: die("unknown command '" + cmd + "'\n" + __doc__)
    except IndexError:
        die("bad args.\n" + __doc__)

if __name__ == "__main__":
    main()
