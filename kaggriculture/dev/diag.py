import sys, multiprocessing as mp
from cand import load
from kaggle_environments import make
def run(seed):
    A = load("ref/closer_cleo.py","A")
    env = make("kaggriculture", configuration={"episodeSteps":720,"seed":seed}, debug=False)
    env.run([A.agent,"starter"])
    out = []
    for d in (1, 3, 6, 12, 20, 29):
        o = env.steps[d*24][0].observation
        f = o["farms"][0]
        an = sum(1 for row in f["tiles"] for c in row if isinstance(c, dict) and "animal" in c)
        weeds = sum(1 for row in f["tiles"] for c in row if isinstance(c, dict) and c.get("kind")=="WEED")
        out.append((d, round(f["money"]), an, weeds))
    return seed, env.steps[-1][0].reward, out
if __name__ == "__main__":
    with mp.Pool(4) as p:
        for seed, r, out in p.map(run, range(1, 13)):
            print(seed, r, out)
