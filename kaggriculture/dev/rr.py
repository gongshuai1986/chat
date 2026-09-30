import sys, itertools, multiprocessing as mp, importlib.util
from kaggle_environments import make

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def game(args):
    a, b, seed, seat = args
    A = load(a, "A"); B = load(b, "B") if b != "starter" else None
    fa, fb = A.agent, (B.agent if B else "starter")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([fa, fb] if seat == 0 else [fb, fa])
    r = env.steps[-1]
    ra, rb = (r[0].reward, r[1].reward) if seat == 0 else (r[1].reward, r[0].reward)
    return ra, rb

def h2h(a, b, seeds, procs=4):
    jobs = [(a, b, s, seat) for s in seeds for seat in (0, 1)]
    with mp.Pool(procs) as p: res = p.map(game, jobs)
    w = sum(1 for x, y in res if x > y); l = sum(1 for x, y in res if x < y)
    return w, l, len(res)-w-l, sum(x for x, _ in res)/len(res), sum(y for _, y in res)/len(res)

if __name__ == "__main__":
    agents = sys.argv[1].split(",")
    seeds = list(range(1, int(sys.argv[2])+1))
    for a, b in itertools.combinations(agents, 2):
        w, l, t, ma, mb = h2h(a, b, seeds)
        print(f"{a.split('/')[-1]:18} vs {b.split('/')[-1]:18} W{w} L{l} T{t}  {ma:9.0f} vs {mb:9.0f}", flush=True)
