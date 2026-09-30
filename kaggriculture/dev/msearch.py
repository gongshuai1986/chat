import json, random, sys, time, copy, multiprocessing as mp
import mutate as M

def sample(rng, tape, g):
    g = copy.deepcopy(g)
    kind = rng.choice(["cutoff", "scale", "shift", "shift", "shift", "hire"])
    if kind == "cutoff":
        k = rng.choice(["SEED", "ANIMAL", "FERT"]); g.setdefault("buy_cutoff", {})[k] = rng.randint(17, 28)
    elif kind == "scale":
        item = rng.choice(["MELON", "STRAWBERRY", "MILK", "WOOL", "FERTILIZER", "WHEAT", "TOMATO", "CARROT", "EGG"])
        d1 = rng.randint(0, 27); d2 = min(30, d1 + rng.choice([1, 2, 3, 5]))
        g.setdefault("sell_scale", []).append([item, d1, d2, rng.choice([0, 0.5, 0.75])])
    elif kind == "hire":
        d1 = rng.randint(0, 27); d2 = min(30, d1 + rng.choice([1, 2, 4]))
        g.setdefault("hire_cap", []).append([d1, d2, rng.randint(3, 13)])
    else:
        cands = [(s, i) for s, st in enumerate(tape) for i, o in enumerate(st["market"])
                 if o and (o[0] in ("BUY_ANIMAL", "BUY_LAND", "BUY_SEED", "SELL"))]
        s, i = rng.choice(cands)
        g.setdefault("shifts", []).append([[s, i], rng.choice([-24, -12, -6, -3, -2, -1, 1, 2, 3, 6, 12, 24])])
    return g, kind

def ev(g, tape, seeds, field, pool, tag):
    path = f"/tmp/mut_{tag}.json"; M.write(M.apply(tape, g), path)
    return M.evaluate(path, seeds, pool, field)

if __name__ == "__main__":
    budget_s = int(sys.argv[1]); out = sys.argv[2]; rng = random.Random(int(sys.argv[3]))
    tape = M.orig_tape(); g = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
    F3 = M.FIELD[:2] + [M.FIELD[4]]
    with mp.Pool(4) as pool:
        bw, n, bm = ev(g, tape, [700, 701], F3, pool, "base"); print("base screen", bw, n, round(bm), flush=True)
        cw, cn, cm = ev(g, tape, [702, 703], M.FIELD, pool, "basec"); print("base confirm", cw, cn, round(cm), flush=True)
        t0 = time.time(); i = 0
        while time.time() - t0 < budget_s:
            i += 1
            cand, kind = sample(rng, tape, g)
            w, n, m = ev(cand, tape, [700, 701], F3, pool, "c")
            if m <= bm + 200: continue
            w2, n2, m2 = ev(cand, tape, [702, 703], M.FIELD, pool, "cc")
            if m2 >= cm and (m + m2) > (bm + cm):
                g, bm, cm = cand, m, m2
                json.dump(g, open(out, "w"))
                print(f"{i} ACCEPT {kind}: screen {w}/{n} {m:.0f} | confirm {w2}/{n2} {m2:.0f}", flush=True)
        print("iters", i, "final", round(bm), round(cm))
