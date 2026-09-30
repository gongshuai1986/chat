import sys, copy, collections, importlib.util
from kaggle_environments import make
import exp
s = importlib.util.spec_from_file_location("P", "plan_agent.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
pol = copy.deepcopy(exp.base)
if sys.argv[1] == "geese":
    pol["animal_target"] = {"COW":10,"SHEEP":3,"GOOSE":10}; pol["animals"] = ["COW","SHEEP","GOOSE"]
    pol["build"] = [{"kind":"PASTURE","target":15,"share":0.5,"from_day":0,"until_day":20},{"kind":"COOP","target":10,"share":0.4,"from_day":0,"until_day":20}]
    pol["sell_order"] = ["EGG"] + pol["sell_order"]
m.POLICY.clear(); m.POLICY.update(pol)
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 3}, debug=False)
env.run([m.agent, "starter"])
for st in env.steps[23::48]:
    o = st[0].observation; f = o["farms"][0]; c = collections.Counter()
    for row in f["tiles"]:
        for t in row:
            if t is None: c["empty"] += 1
            elif t == "LOCKED": c["locked"] += 1
            elif isinstance(t, dict):
                c[t.get("type") or t.get("kind") or "?"] += 1
    print(f"d{o['day']:2} money {f['money']:7.0f} hands {len(f['hands']):2} quad {len(f['unlocked_quadrants'])} {dict(c)}")
print("reward", env.steps[-1][0].reward)
