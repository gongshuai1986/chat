import sys, glob, json
from cand import evaluate
seeds = list(range(1, int(sys.argv[1]))) if len(sys.argv) > 1 else [1,2,3]
paths = sys.argv[2:] or sorted(glob.glob("tapes/*.json"))
for p in paths:
    meta = json.load(open(p)); meta.pop("tape")
    w, tot, m, out = evaluate({"TAPE_PATH": p}, seeds, base="tape_agent.py")
    print(f"{p:26} {meta['team'][:16]:16} orig {meta['reward']:8.0f} | win {w}/{tot} margin {m:8.0f}", {k: v[0] for k, v in out.items()}, flush=True)
