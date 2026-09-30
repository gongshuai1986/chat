import sys, glob, json, itertools, multiprocessing as mp, importlib.util, copy
from kaggle_environments import make
from collections import defaultdict

def load_agent(spec):
    if spec.startswith("tape:"):
        path = spec[5:]
        s = importlib.util.spec_from_file_location("t_"+str(abs(hash(spec))), "tape_agent.py")
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m); m.TAPE_PATH = path
        return m.agent
    if spec.startswith("cleo:"):
        s = importlib.util.spec_from_file_location("c_"+str(abs(hash(spec))), "ref/closer_cleo.py")
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        m._TRACE = json.load(open(spec[5:]))["tape"] + [{"farmer": ["PASS"], "hands": [], "market": []}]
        return m.agent
    s = importlib.util.spec_from_file_location("x_"+str(abs(hash(spec))), spec)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.agent

def game(args):
    a, b, seed, seat = args
    fa, fb = load_agent(a), load_agent(b)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([fa, fb] if seat == 0 else [fb, fa])
    r = env.steps[-1]
    return a, b, r[seat].reward, r[1-seat].reward

def label(s):
    if s.startswith("tape:") or s.startswith("cleo:"):
        m = json.load(open(s[5:])); return f"{s[:4]}-{m['team'][:8]}_{m['episode']}_{s[-6]}"
    return s.split('/')[-1][:-3]

if __name__ == "__main__":
    specs = sys.argv[2:]; seeds = list(range(int(sys.argv[1].split(":")[0]), int(sys.argv[1].split(":")[0]) + int(sys.argv[1].split(":")[1])))
    jobs = [(a, b, s, seat) for a, b in itertools.combinations(specs, 2) for s in seeds for seat in (0, 1)]
    with mp.Pool(4) as p: res = p.map(game, jobs, chunksize=2)
    W = defaultdict(int); G = defaultdict(int); M = defaultdict(float); pair = defaultdict(lambda: [0, 0])
    for a, b, ra, rb in res:
        for x, y, rx, ry in ((a, b, ra, rb), (b, a, rb, ra)):
            G[x] += 1; W[x] += rx > ry; M[x] += rx - ry
        pair[(a, b)][0] += ra > rb; pair[(a, b)][1] += rb > ra
    order = sorted(specs, key=lambda s: -W[s] / G[s])
    for s in order: print(f"{label(s):28} win {W[s]:3}/{G[s]:3} = {W[s]/G[s]:.2f} margin {M[s]/G[s]:8.0f}")
    json.dump({f"{a}|{b}": v for (a, b), v in pair.items()}, open("/tmp/pair_results.json", "w"))
