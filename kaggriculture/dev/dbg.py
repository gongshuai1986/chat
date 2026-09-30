import sys, json, copy
from harness import load
from kaggle_environments import make
import sweep4 as sweep2
A = load("base_rita.py","A")
A.POLICY.update(sweep2.configs[sys.argv[1]])
env = make("kaggriculture", configuration={"episodeSteps":720,"seed":1}, debug=False)
env.run([A.agent,"starter"])
for t in range(0,720,24*int(sys.argv[2]) if len(sys.argv)>2 else 48):
    o = env.steps[t][0].observation
    f = o.farms[0] if hasattr(o,'farms') else o["farms"][0]
    tiles = f["tiles"]
    cnt = {}
    for row in tiles:
        for c in row:
            k = "LOCKED" if c=="LOCKED" else (c["kind"] if isinstance(c,dict) else "EMPTY")
            if isinstance(c,dict) and "animal" in c: k += "+"+c["animal"]
            cnt[k]=cnt.get(k,0)+1
    priv = o["private"] if not hasattr(o,"private") else o.private
    sh={k:v for k,v in priv["shed"].items() if v}
    print(t//24, round(f["money"]), cnt, sh, priv["seeds"])
