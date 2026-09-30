import sys, json, multiprocessing as mp, importlib.util, copy
from kaggle_environments import make

BASE = "ref/closer_cleo.py"
POOL = ["ref/broker_bea.py","ref/ledger_lena.py","ref/slotter_silas.py","ref/closer_cleo.py"]

def load(path, name, patch=None):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for k, v in (patch or {}).items(): setattr(m, k, copy.deepcopy(v))
    return m

def game(args):
    base, patch, opp, seed, seat = args
    A = load(base, "A", patch); B = load(opp, "B")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([A.agent, B.agent] if seat == 0 else [B.agent, A.agent])
    r = env.steps[-1]
    return (r[seat].reward, r[1-seat].reward)

def evaluate(patch, seeds, pool=POOL, base=BASE, procs=4):
    jobs = [(base, patch, o, s, seat) for o in pool for s in seeds for seat in (0, 1)]
    with mp.Pool(procs) as p: res = p.map(game, jobs)
    n = len(seeds) * 2; out = {}
    for i, o in enumerate(pool):
        r = res[i*n:(i+1)*n]
        out[o.split('/')[-1][:-3]] = (sum(a > b for a, b in r), sum(a - b for a, b in r)/n)
    w = sum(v[0] for v in out.values()); tot = n*len(pool)
    return w, tot, sum(v[1] for v in out.values())/len(out), out

if __name__ == "__main__":
    patch = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    seeds = list(range(1, int(sys.argv[2])+1)) if len(sys.argv) > 2 else list(range(1, 7))
    for k, v in patch.items():
        if isinstance(v, list): patch[k] = tuple(v)
    w, tot, m, out = evaluate(patch, seeds)
    print(f"win {w}/{tot} margin {m:8.0f}", {k: v[0] for k, v in out.items()})
