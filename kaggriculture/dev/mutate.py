import json, copy, random, sys, os, multiprocessing as mp, importlib.util
from kaggle_environments import make

SRC = "tapes/115469228_1.json"
FIELD = ["tape:tapes/115464540_0.json", "tape:tapes/115474317_0.json", "tape:tapes/115469223_1.json",
         "tape:tapes/115456508_1.json", "tape:tapes/115469228_1.json"]

def orig_tape():
    return json.load(open(SRC))["tape"] + [{"farmer": ["PASS"], "hands": [], "market": []}]

def apply(tape, g):
    t = copy.deepcopy(tape)
    for d, d2, cap in g.get("hire_cap", []):
        for day in range(d, d2):
            left = cap
            for s in range(day * 24, min(day * 24 + 24, len(t))):
                m = t[s]["market"]
                for i, o in enumerate(m):
                    if o and o[0] == "HIRE":
                        if left > 0: left -= 1
                        else: m[i] = ["NOOP"]
    for kind, day in g.get("buy_cutoff", {}).items():
        for s in range(int(day) * 24, len(t)):
            m = t[s]["market"]
            for i, o in enumerate(m):
                if o and ((kind == "SEED" and o[0] == "BUY_SEED") or (kind == "ANIMAL" and o[0] == "BUY_ANIMAL")
                          or (kind == "FERT" and o[0] == "BUY_PRODUCT" and o[1] == "FERTILIZER")):
                    m[i] = ["NOOP"]
    for item, d1, d2, f in g.get("sell_scale", []):
        for s in range(d1 * 24, min(d2 * 24, len(t))):
            for o in t[s]["market"]:
                if o and o[0] == "SELL" and o[1] == item:
                    o[2] = max(0, int(round(o[2] * f))) if f < 50 else o[2]
    moves = []
    for (s, i), dt in g.get("shifts", []):
        if s < len(t) and i < len(t[s]["market"]) and t[s]["market"][i] and t[s]["market"][i][0] != "NOOP":
            moves.append((s, i, dt))
    for s, i, dt in moves:
        if i >= len(t[s]["market"]): continue
        o = t[s]["market"][i]
        if not o or o[0] == "NOOP": continue
        s2 = min(max(0, s + dt), len(t) - 2)
        t[s]["market"][i] = ["NOOP"]
        m2 = t[s2]["market"]
        free = [k for k, x in enumerate(m2) if x and x[0] == "NOOP"]
        if free: m2[free[0]] = o
        elif len(m2) < 10: m2.append(o)
        else: t[s]["market"][i] = o
    return t

def write(tape, path):
    json.dump({"team": "mut", "episode": 0, "reward": 0, "tape": tape}, open(path, "w"), separators=(",", ":"))

def load_agent(spec):
    if spec.startswith("cleo:"):
        s = importlib.util.spec_from_file_location("c"+str(abs(hash(spec))), "ref/closer_cleo.py")
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        m._TRACE = json.load(open(spec[5:]))["tape"]
        if len(m._TRACE) < 720: m._TRACE.append({"farmer": ["PASS"], "hands": [], "market": []})
        return m.agent
    s = importlib.util.spec_from_file_location("t"+str(abs(hash(spec))), "tape_agent.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); m.TAPE_PATH = spec[5:]; return m.agent

def game(a):
    me, opp, seed, seat = a
    fa, fb = load_agent(me), load_agent(opp)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([fa, fb] if seat == 0 else [fb, fa])
    r = env.steps[-1]; return r[seat].reward, r[1-seat].reward

def evaluate(path, seeds, pool, field=FIELD):
    res = pool.map(game, [("cleo:" + path, o, s, seat) for o in field for s in seeds for seat in (0, 1)])
    return sum(1 for a, b in res if a > b), len(res), sum(a - b for a, b in res) / len(res)
