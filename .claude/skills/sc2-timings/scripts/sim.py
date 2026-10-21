#!/usr/bin/env python3
"""Build-order simulator on top of data/sc2_data.json (Protoss and Terran).

Usage: sim.py <build.txt> [--rate 54] [--trace]

Build file: one step per line, executed strictly in order (a step blocks the next
until it starts). '#' starts a comment. 'race Terran' and 'end 7:30' are optional headers.

  <trigger> <action> [save]
  trigger:  14        when supply used reaches 14
            1:38      at or after this clock time
            -         as soon as the previous step has started
  action:   Pylon | Gateway | Nexus | ...      build (a worker walks; a Nexus is the natural)
            Zealot | Stalker x2 | ...          train, or warp in from a ready Warp Gate
            Warp Gate (research) | Charge      research at its building
            Orbital Command                    morph
            Reactor on Barracks | Tech Lab on Factory
            chrono <Building>                  next 50 Nexus energy goes on a busy one
            autochrono <Building>, <Building>  any Nexus at 50 energy boosts the first busy one
            workers <N|on>                     cap workers at N (0 stops them)
            scout <seconds>                    one worker leaves minerals for that long
            recharge                           Energy Recharge: spends 50 Nexus energy
            gas <N>                            at most N workers on gas
            gas <N>+<M>                        N on gas, plus up to M more once minerals hold
                                               16 per finished base
            loop <Unit> [<Unit> ...]           every free producer keeps making these; a step
                                               waiting for money reserves its cost first, then
                                               earlier units reserve theirs before later ones
            loop first <Unit> [...]            same, but ahead of the build steps
            bank <minerals>                    wait until the bank holds this much (use with save)
            keep gateways                      stop the default auto-transform to Warp Gate
            autosupply                         Pylon/Depot whenever supply runs short
            report                             print the state at the trigger time
  'save' stops worker production while that step waits for money.

Model (Faster seconds): minerals 54/min per worker for the first 16 on a base and 35/min
for workers 17-24, gas 54/min per worker (3 per geyser), fitted to replays (see the DB's
constants.mining). Workers
split evenly across finished bases. A Protoss builder is off minerals 6s (14s for a Nexus),
a Terran builder for the whole build. Chrono +50% for 20s. MULE ~225 over 64s. Warp-in
3.6s in a fast field, cooldown runs during it. Gateways auto-transform once Warp Gate
research is done (the in-game default). Output is clean-execution timing: a real
game lands a few seconds later per step.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc2db import load, lookup, mmss, parse_mmss

DT = 0.05
args = sys.argv[1:]
TRACE = '--trace' in args
RATE = float(args[args.index('--rate') + 1]) if '--rate' in args else 54.0
R1, R2, RG = RATE / 60, 35 / 60, 54 / 60
db = load()
WG = db['constants']['macro_mechanics']['WarpGate']
TOWN = {'Nexus', 'Command Center', 'Orbital Command', 'Planetary Fortress'}
GASB = {'Assimilator', 'Refinery'}
PROD = {'Gateway', 'Warp Gate', 'Robotics Facility', 'Stargate', 'Barracks', 'Factory', 'Starport'}
_cache = {}


def ent(name):
    if name not in _cache:
        c, r, e = lookup(db, name)
        if not e:
            sys.exit('unknown: ' + name)
        _cache[name] = (c, r, e)
    return _cache[name]


class B:
    def __init__(s, typ, done):
        s.typ, s.done, s.item, s.left, s.chrono = typ, done, None, 0.0, -1.0
        s.energy = 50.0 if typ in ('Nexus', 'Orbital Command') else 0.0
        s.addon, s.extra, s.cd = None, [], 0.0


class Sim:
    def __init__(s, race, steps):
        s.race, s.steps, s.i = race, steps, 0
        s.t, s.m, s.g = 0.0, 50.0, 0.0
        s.workers, s.wprod, s.wcap, s.gascap, s.gasextra = 12, 0, 80, 99, 0
        s.used, s.away = 12, []
        s.b = [B('Nexus' if race == 'Protoss' else 'Command Center', 0.0)]
        s.ups, s.upprog = {}, set()
        s.loops, s.autosupply, s.autochrono = [], False, []
        s.mule, s.log, s.units = [], [], []
        s.mined = 0.0
        s.keepgates = False
        s.loopfirst = False

    # ---- state -------------------------------------------------------------
    def up(s, x):
        return x.done <= s.t

    def ready(s, typ):
        return [x for x in s.b if x.typ == typ and s.up(x)]

    def cap(s, incl=False):
        tot = 0
        for x in s.b:
            if incl or s.up(x):
                e = lookup(db, x.typ)[2]
                tot += e.get('provides_supply', 0) if e else 0
        return min(200, tot)

    def have(s, name):
        if name in s.ups:
            return s.ups[name] <= s.t
        if name == 'Gateway':
            return any(x.typ in ('Gateway', 'Warp Gate') and s.up(x) for x in s.b)
        if name in ('Command Center', 'Nexus'):
            return any(x.typ in TOWN and s.up(x) for x in s.b)
        return any(x.typ == name and s.up(x) for x in s.b)

    def free_workers(s):
        return s.workers - sum(n for u, n in s.away if u > s.t)

    def income(s):
        bases = max(1, len([x for x in s.b if x.typ in TOWN and s.up(x)]))
        geys = len([x for x in s.b if x.typ in GASB and s.up(x)])
        free = s.free_workers()
        gw = max(0, min(3 * geys, free - 1, s.gascap))
        if s.gasextra:
            # extra gas workers only once every finished base has 16 on minerals
            gw = min(3 * geys, gw + max(0, min(s.gasextra, free - gw - 16 * bases)))
        per = (free - gw) / bases
        f = (min(per, 16) * R1 + max(0.0, min(per, 24) - 16) * R2) * bases
        f += 3.52 * len([u for u in s.mule if u > s.t])
        return f, gw * RG

    def busy(s, x):
        return x.item is not None or x.cd > 0

    # ---- production ---------------------------------------------------------
    def producer_for(s, e):
        names = [p.split(' (')[0].strip() for p in e['from'].split(' / ')]
        if any(n.startswith('Orbital') or n.startswith('Command') for n in names):
            names += ['Command Center', 'Orbital Command', 'Planetary Fortress']
        lab = any(r.endswith('Tech Lab') for r in e.get('req', []))
        for x in s.b:
            if not s.up(x):
                continue
            if x.typ == 'Warp Gate' and 'Gateway' in names:
                if x.cd <= 0:
                    return x
                continue
            if x.typ not in names:
                continue
            if lab and x.addon != 'Tech Lab':
                continue
            if x.item and x.item.startswith('@'):
                continue
            cap = 2 if x.addon == 'Reactor' and not lab else 1
            if (1 if x.item else 0) + len(x.extra) < cap:
                return x
        return None

    def unit_ok(s, e, rm=0.0, rg=0.0):
        if s.used + e['supply'] > s.cap():
            return None
        if s.m < e['mins'] + rm or s.g < e['gas'] + rg:
            return None
        if not all(s.have(r) for r in e.get('req', []) if not r.endswith('Tech Lab')):
            return None
        return s.producer_for(e)

    def start_unit(s, x, name, e):
        s.m -= e['mins']; s.g -= e['gas']; s.used += e['supply']
        if x.typ == 'Warp Gate':
            x.cd = WG['cooldown_faster_s'].get(name, 20.0)
            s.units.append((name, s.t + WG['warp_in_time_faster_s']['fast_field']))
        elif x.item is None:
            x.item, x.left = name, float(e['bt_faster'])
        else:
            x.extra.append([name, float(e['bt_faster'])])

    def finish(s, x, name):
        if name in ('Probe', 'SCV'):
            s.workers += 1; s.wprod -= 1
        elif name.startswith('@'):
            kind, what = name[1:].split(':', 1)
            if kind == 'up':
                s.ups[what] = s.t; s.upprog.discard(what)
            elif kind == 'addon':
                x.addon = what
                s.b.append(B(x.typ + ' ' + what, s.t))
            elif kind == 'morph':
                x.typ = what
                if what == 'Orbital Command':
                    x.energy = 50.0
        else:
            s.units.append((name, s.t))

    def tick(s):
        if not s.keepgates and s.have('Warp Gate (research)'):
            for x in s.b:
                if x.typ == 'Gateway' and s.up(x) and x.item is None:
                    x.typ, x.cd = 'Warp Gate', float(WG['transform_duration_faster_s'])
        for x in s.b:
            if not s.up(x):
                continue
            sp = 1.5 if x.chrono > s.t else 1.0
            if x.cd > 0:
                x.cd -= DT * sp
            if x.item:
                x.left -= DT * sp
                if x.left <= 0:
                    it, x.item = x.item, None
                    s.finish(x, it)
            for ex in list(x.extra):
                ex[1] -= DT * sp
                if ex[1] <= 0:
                    x.extra.remove(ex); s.finish(x, ex[0])
            if x.typ in ('Nexus', 'Orbital Command'):
                x.energy = min(200.0, x.energy + 0.7875 * DT)

    def build(s, name, e):
        if s.m < e['mins'] or s.g < e['gas'] or s.free_workers() < 2:
            return False
        if not all(s.have(r) for r in e.get('req', [])):
            return False
        s.m -= e['mins']; s.g -= e['gas']
        bt = float(e['bt_faster'])
        s.away.append((s.t + (bt + 4 if s.race == 'Terran' else (14 if name == 'Nexus' else 6)), 1))
        s.b.append(B(name, s.t + bt))
        return True

    def cost(s, a):
        a = re.sub(r' x\d+$', '', a)
        m = re.match(r'(Reactor|Tech Lab) on ', a)
        if m:
            a = m.group(1) + ' (add-on)'
        c, r, e = lookup(db, a)
        return (e['mins'], e['gas']) if e else (0, 0)

    def chrono_on(s, nx, tgt):
        tg = [x for x in s.b if x.typ == tgt and s.up(x) and s.busy(x) and x.chrono <= s.t]
        if not tg:
            return False
        nx.energy -= 50; tg[0].chrono = s.t + 20.0
        return True

    def do(s, st):
        a = st['act']
        if a == 'report':
            s.log.append((s.t, None, s.report())); return True
        if a.startswith('workers '):
            v = a.split()[1]; s.wcap = 80 if v == 'on' else int(v); return True
        if a.startswith('bank '):
            return s.m >= float(a.split()[1])
        if a == 'keep gateways':
            s.keepgates = True; return True
        if a == 'recharge':
            nx = [x for x in s.ready('Nexus') if x.energy >= 50]
            if not nx:
                return False
            nx[0].energy -= 50; return True
        if a.startswith('scout '):
            s.away.append((s.t + float(a.split()[1]), 1)); return True
        if a.startswith('gas '):
            v = a.split()[1]
            first, _, extra = v.partition('+')
            s.gascap, s.gasextra = int(first), int(extra or 0); return True
        if a.startswith('loop '):
            s.loops = a.split(None, 1)[1].replace(',', ' ').split()
            s.loopfirst = s.loops[0] == 'first'
            if s.loopfirst:
                s.loops = s.loops[1:]
            return True
        if a == 'autosupply':
            s.autosupply = True; return True
        if a.startswith('autochrono '):
            s.autochrono = [n.strip() for n in a.split(None, 1)[1].split(',')]; return True
        if a == 'transform':
            if not s.have('Warp Gate (research)'):
                return False
            for x in s.b:
                if x.typ == 'Gateway' and s.up(x) and x.item is None:
                    x.typ, x.cd = 'Warp Gate', float(WG['transform_duration_faster_s'])
            return True
        if a.startswith('chrono '):
            return any(s.chrono_on(nx, a[7:].strip()) for nx in s.ready('Nexus') if nx.energy >= 50)
        m = re.match(r'(Reactor|Tech Lab) on (.+)', a)
        if m:
            kind, host = m.groups()
            e = ent(kind + ' (add-on)')[2]
            hs = [x for x in s.ready(host) if x.item is None and x.addon is None and not x.extra]
            if not hs or s.m < e['mins'] or s.g < e['gas']:
                return False
            s.m -= e['mins']; s.g -= e['gas']
            hs[0].item, hs[0].left = '@addon:' + kind, float(e['bt_faster']); return True
        n = 1
        mx = re.match(r'(.+?) x(\d+)$', a)
        if mx:
            a, n = mx.group(1), int(mx.group(2))
        c, r, e = ent(a)
        if c == 'upgrades':
            at = e['at'].split(' / ')[0].strip()
            hs = [x for x in s.ready(at) if x.item is None]
            if a in s.ups or a in s.upprog or not hs or s.m < e['mins'] or s.g < e['gas']:
                return False
            if not all(s.have(q) for q in e.get('req', [])):
                return False
            s.m -= e['mins']; s.g -= e['gas']; s.upprog.add(a)
            hs[0].item, hs[0].left = '@up:' + a, float(e['rt_faster']); return True
        if c == 'buildings':
            if e.get('morph_from') and a != 'Warp Gate':
                hs = [x for x in s.ready(e['morph_from']) if x.item is None]
                if not hs or s.m < e['mins'] or s.g < e['gas'] or not all(s.have(q) for q in e.get('req', [])):
                    return False
                s.m -= e['mins']; s.g -= e['gas']
                hs[0].item, hs[0].left = '@morph:' + a, float(e['bt_faster']); return True
            return s.build(a, e)
        st.setdefault('made', 0)
        while st['made'] < n:
            x = s.unit_ok(e)
            if not x:
                return False
            s.start_unit(x, a, e); st['made'] += 1
        return True

    def reserve(s, cm, cg):
        # What must stay banked now so an item costing cm/cg is not delayed: only the part
        # that income will not refill before the scarcer resource arrives anyway.
        f, g = s.income()
        t = max((cm - s.m) / f if f > 0 else (0 if s.m >= cm else 1e9),
                (cg - s.g) / g if g > 0 else (0 if s.g >= cg else 1e9), 0.0)
        return max(0.0, cm - f * t) if t < 1e8 else cm, max(0.0, cg - g * t) if t < 1e8 else cg

    def run_loops(s, rm=0.0, rg=0.0):
        # Units are in priority order: a higher one whose producer is free but which
        # cannot be afforded yet reserves its cost before lower ones may spend. A build
        # step that is waiting for money reserves its cost first (rm, rg).
        for u in s.loops:
            e = ent(u)[2]
            x = s.unit_ok(e, rm, rg)
            while x:
                s.start_unit(x, u, e); x = s.unit_ok(e, rm, rg)
            if s.producer_for(e) and s.used + e['supply'] <= s.cap() and all(
                    s.have(r) for r in e.get('req', []) if not r.endswith('Tech Lab')):
                am, ag = s.reserve(e['mins'] + rm, e['gas'] + rg)
                rm, rg = max(rm, am), max(rg, ag)

    def triggered(s, st):
        tr = st['trig']
        if tr is None:
            return True
        return s.t >= tr if isinstance(tr, float) else s.used >= tr

    def report(s):
        f, g = s.income()
        army = [u for u, born in s.units if born <= s.t]
        cnt = {}
        for u in army:
            cnt[u] = cnt.get(u, 0) + 1
        val = sum(ent(u)[2]['mins'] + ent(u)[2]['gas'] for u in army)
        sup = sum(ent(u)[2]['supply'] for u in army)
        bases = len([x for x in s.b if x.typ in TOWN and s.up(x)])
        gates = len([x for x in s.b if x.typ in PROD and s.up(x)])
        return (f"report: supply {s.used}/{s.cap()}, workers {s.workers}, bases {bases}, producers {gates}, "
                f"army {sup} supply = {val} value {cnt}, bank {int(s.m)}m {int(s.g)}g, "
                f"income {int(f * 60)}m {int(g * 60)}g per min, mined {int(s.mined)}m")

    def run(s, end):
        while s.t <= end:
            f, g = s.income()
            if s.t >= 2.0:
                s.m += f * DT; s.mined += f * DT
            s.g += g * DT
            s.tick()
            for x in s.ready('Orbital Command'):
                if x.energy >= 50 and x.item is None:
                    x.energy -= 50; s.mule.append(s.t + 64)
            if s.autochrono:
                for nx in s.ready('Nexus'):
                    if nx.energy >= 50:
                        any(s.chrono_on(nx, tg) for tg in s.autochrono)
            if s.autosupply and s.cap(True) < 200:
                prods = len([x for x in s.b if x.typ in PROD])
                towns = len([x for x in s.b if x.typ in TOWN])
                pending = len([x for x in s.b if x.typ in ('Pylon', 'Supply Depot') and not s.up(x)])
                if s.cap(True) - s.used < 4 + 2 * prods + 2 * towns and pending < 1 + (prods + 1) // 3:
                    nm = 'Pylon' if s.race == 'Protoss' else 'Supply Depot'
                    if s.build(nm, ent(nm)[2]):
                        s.log.append((s.t, s.used, nm + ' (auto)'))
            if s.loops and s.loopfirst:
                s.run_loops()
            saving = waiting = False
            wm = wg = 0.0
            while s.i < len(s.steps):
                st = s.steps[s.i]
                if not s.triggered(st):
                    break
                if s.do(st):
                    if st['act'] != 'report':
                        s.log.append((s.t, s.used, st['raw']))
                    s.i += 1
                    continue
                cm, cg = s.cost(st['act'])
                if st['act'].startswith('bank '):
                    cm = float(st['act'].split()[1])
                waiting = s.m < cm or s.g < cg
                wm, wg = s.reserve(cm, cg) if waiting else (0.0, 0.0)
                saving = st['save'] and waiting
                break
            if not saving:
                wk = 'Probe' if s.race == 'Protoss' else 'SCV'
                for x in s.b:
                    if x.typ in TOWN and s.up(x) and x.item is None and s.workers + s.wprod < s.wcap \
                            and s.m >= 50 and s.used < s.cap():
                        s.m -= 50; s.used += 1; s.wprod += 1; x.item, x.left = wk, 12.0
            if s.loops and not s.loopfirst:
                s.run_loops(wm, wg)
            s.away = [(u, n) for u, n in s.away if u > s.t]
            s.t = round(s.t + DT, 3)


def parse(path):
    race, steps, end = 'Protoss', [], 420.0
    for raw in open(path):
        line = raw.split('#')[0].strip()
        if not line:
            continue
        if line.startswith('race '):
            race = line.split()[1].capitalize(); continue
        if line.startswith('end '):
            end = float(parse_mmss(line.split()[1])); continue
        trig, act = line.split(None, 1)
        if trig != '-' and not re.match(r'^\d+(:\d\d)?$', trig):
            trig, act = '-', line
        save = act.endswith(' save')
        if save:
            act = act[:-5].strip()
        t = None if trig == '-' else (float(parse_mmss(trig)) if ':' in trig else int(trig))
        steps.append({'trig': t, 'act': act, 'save': save, 'raw': act})
    return race, steps, end


if __name__ == '__main__':
    if not args or args[0].startswith('--'):
        print(__doc__); sys.exit(1)
    race, steps, end = parse(args[0])
    s = Sim(race, steps)
    s.run(end)
    for t, used, what in s.log:
        if used is None:
            print(f"{mmss(t):>6}       {what}")
        elif TRACE or '(auto)' not in what:
            print(f"{mmss(t):>6} {used:>4}  {what}")
    if s.i < len(steps):
        print(f"  !! never started step {s.i + 1}: {steps[s.i]['raw']}")
