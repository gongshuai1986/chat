import sys, json, copy, importlib.util
from kaggle_environments import make
import exp
s = importlib.util.spec_from_file_location("P", "plan_agent.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
pol = copy.deepcopy(exp.base)
if len(sys.argv) > 1 and sys.argv[1] == "geese":
    pol["animal_target"] = {"COW":10,"SHEEP":3,"GOOSE":10}; pol["animals"] = ["COW","SHEEP","GOOSE"]
    pol["build"] = [{"kind":"PASTURE","target":15,"share":0.5,"from_day":0,"until_day":20},{"kind":"COOP","target":10,"share":0.4,"from_day":0,"until_day":20}]
    pol["sell_order"] = ["EGG"] + pol["sell_order"]
m.POLICY.clear(); m.POLICY.update(pol)
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 3}, debug=False)
env.run([m.agent, "starter"])
for st in env.steps[::48]:
    o = st[0].observation
    me = o.get("players", [{}])[0] if isinstance(o, dict) else None
    print(o.get("step"), {k: (v if not isinstance(v,(list,dict)) else len(v)) for k, v in (o.get("private") or {}).items()} if o.get("private") else "", flush=True)
print("reward", env.steps[-1][0].reward)
