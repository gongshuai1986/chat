import json, random, time, multiprocessing as mp
import mutate as M
from msearch import sample, ev
rng = random.Random(99); tape = M.orig_tape()
F3 = M.FIELD[:2] + [M.FIELD[4]]
rows = []
with mp.Pool(4) as pool:
    bw, n, bm = ev({}, tape, [700, 701], F3, pool, "b"); print("base", bw, n, round(bm))
    t0 = time.time()
    while time.time() - t0 < 560:
        cand, kind = sample(rng, tape, {})
        w, n, m = ev(cand, tape, [700, 701], F3, pool, "c")
        rows.append((kind, round(m - bm), w - bw)); print(kind, round(m - bm), w - bw, flush=True)
from collections import defaultdict
d = defaultdict(list)
for k, dm, dw in rows: d[k].append(dm)
for k, v in d.items():
    print(k, "n", len(v), "zero", sum(1 for x in v if x == 0), "pos", sum(1 for x in v if x > 0), "neg", sum(1 for x in v if x < 0), "best", max(v), "worst", min(v))
