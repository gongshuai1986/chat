import importlib.util, sys, json, copy, multiprocessing as mp
from kaggle_environments import make

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def play(args):
    a_path, b_path, seed, overrides = args
    A = load(a_path, "A")
    if overrides and hasattr(A, "POLICY"):
        A.POLICY.update(copy.deepcopy(overrides))
    if b_path == "starter":
        B = "starter"
    else:
        B = load(b_path, "B").agent
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([A.agent, B])
    s = env.steps[-1]
    return s[0].reward, s[1].reward

def evaluate(a_path, opp_paths, seeds, overrides=None, procs=8):
    jobs = [(a_path, o, s, overrides) for o in opp_paths for s in seeds]
    with mp.Pool(procs) as p:
        res = p.map(play, jobs)
    out = {}
    i = 0
    for o in opp_paths:
        r = res[i:i+len(seeds)]; i += len(seeds)
        out[o] = (sum(x[0] for x in r)/len(r), sum(x[1] for x in r)/len(r), sum(1 for x in r if x[0] > x[1]), len(r))
    return out

if __name__ == "__main__":
    a = sys.argv[1]
    ov = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    opps = ["starter"]
    print(evaluate(a, opps, [1,2,3,4,5,6], ov))
