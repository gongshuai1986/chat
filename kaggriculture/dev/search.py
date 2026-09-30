import sys, json, random, copy, multiprocessing as mp, importlib.util
from kaggle_environments import make

def load():
    s = importlib.util.spec_from_file_location("P", "plan_agent.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def game(args):
    pol, seed = args
    m = load(); m.POLICY.clear(); m.POLICY.update(copy.deepcopy(pol))
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([m.agent, "starter"])
    return env.steps[-1][0].reward or 0

def score(pol, seeds, pool):
    res = pool.map(game, [(pol, s) for s in seeds])
    return 0.7 * sum(res) / len(res) + 0.3 * min(res), min(res)

BASE = dict(hands=9, land=2, land_buffer=800, build=[{"kind":"PASTURE","target":16,"share":0.5,"from_day":0,"until_day":20}],
  animals=["COW","SHEEP"], animal_target={"COW":10,"SHEEP":6}, animal_batch=2, animal_buffer=400, animal_floor=10, land_after_animals=10,
  feed_float_days=8, animals_from_day=1, care=True, animal_harvest_at=2, collect_fertilizer=True, persistent_routing=True, batched_restock=True,
  crops=["WHEAT"], crop_share={"WHEAT":1.0}, seed_batch=16, seed_stock=16, seed_buffer=300, feed_days=2, wheat_batch=24, max_wheat_price=55, carry=8,
  sell_order=["MILK","WOOL","FERTILIZER","WHEAT"], sell_chunk=20, shed_pressure=80, invest_until_day=22, plant_until_day=25, liquidate_from_day=28)

def sample(rng, best):
    p = copy.deepcopy(best)
    def pick(key, choices): p[key] = rng.choice(choices)
    k = rng.randint(1, 4)
    knobs = ["hands","land_days","cow","sheep","goose","crops","feed_float","seed","buffers","sell","fert","carry","hands_by_day","floor","floor","layout","layout","crops","crops","land_days"]
    for kn in rng.sample(knobs, k):
        if kn == "hands": pick("hands", [7,8,9,10,11,12,13])
        elif kn == "hands_by_day":
            p.pop("hands", None); p["hands_by_day"] = [(0, rng.choice([3,5,7])), (rng.choice([3,5,7]), rng.choice([8,10,12])), (rng.choice([9,11,13]), rng.choice([10,12,14]))]
        elif kn == "land_days": p["land_days"] = sorted(rng.sample(range(2, 16), rng.choice([1,2,3,3])))
        elif kn in ("cow","sheep"):
            p["animal_target"] = dict(p["animal_target"]); p["animal_target"]["COW" if kn=="cow" else "SHEEP"] = rng.choice([0,3,5,8,10,12,14])
        elif kn == "goose":
            n = rng.choice([0, 4, 6, 8, 12]); p["animal_target"] = dict(p["animal_target"]); p["animal_target"]["GOOSE"] = n
            p["animals"] = ["COW","SHEEP","GOOSE"] if n else ["COW","SHEEP"]
            past = rng.choice([0.25, 0.3, 0.4]); coop = rng.choice([0.1, 0.15, 0.2])
            p["build"] = [{"kind":"PASTURE","target":p["animal_target"].get("COW",0)+p["animal_target"].get("SHEEP",0)+2,"share":past,"from_day":0,"until_day":20}] + ([{"kind":"COOP","target":n+1,"share":coop,"from_day":0,"until_day":20}] if n else [])
            if n: p["sell_order"] = ["EGG"] + [x for x in p["sell_order"] if x != "EGG"]
        elif kn == "layout":
            p["build"] = [dict(b) for b in p["build"]]
            for b in p["build"]:
                b["share"] = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]) if b["kind"] == "PASTURE" else rng.choice([0.1, 0.15, 0.2, 0.3])
        elif kn == "crops":
            opts = [["WHEAT"], ["WHEAT","STRAWBERRY"], ["WHEAT","MELON"], ["WHEAT","STRAWBERRY","MELON"], ["WHEAT","TOMATO"], ["WHEAT","CARROT"], ["WHEAT","STRAWBERRY","TOMATO"]]
            c = rng.choice(opts); p["crops"] = c
            shares = {"WHEAT": rng.choice([0.4,0.5,0.6,0.7])}
            rest = [x for x in c if x != "WHEAT"]
            for x in rest: shares[x] = (1 - shares["WHEAT"]) / len(rest)
            p["crop_share"] = shares
            p["plant_until"] = {"STRAWBERRY": rng.choice([8,10,12]), "MELON": rng.choice([10,12,14]), "TOMATO": rng.choice([12,14,16]), "CARROT": 25, "WHEAT": 25}
            sells = [x for x in ["MELON","STRAWBERRY","MILK","WOOL","EGG","TOMATO","CARROT","FERTILIZER","WHEAT"] if x in c or x in ("MILK","WOOL","FERTILIZER","EGG")]
            p["sell_order"] = sells; p["max_sell_orders"] = 6
            if "MELON" in c and rng.random() < 0.5: p["fertilize_crops"] = ["MELON"]; p["fert_stock"] = 6
        elif kn == "feed_float": pick("feed_float_days", [4,6,8,10])
        elif kn == "seed": p["seed_stock"] = rng.choice([8,12,16,24]); p["seed_batch"] = p["seed_stock"]
        elif kn == "buffers": pick("animal_buffer", [0,200,400,800]); pick("seed_buffer", [100,300,600]); pick("land_buffer", [200,500,800])
        elif kn == "sell": p["sell_chunk"] = rng.choice([10,20,40,80]); p["shed_pressure"] = rng.choice([60,80,95])
        elif kn == "fert": p["collect_fertilizer"] = rng.choice([True, False])
        elif kn == "carry": pick("carry", [4,6,8,12])
    return p

if __name__ == "__main__":
    budget = int(sys.argv[1]); out = sys.argv[2]
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    seeds = [1,2,3,4,5,6,7,8]
    with mp.Pool(4) as pool:
        best = json.load(open(sys.argv[4]))["policy"] if len(sys.argv) > 4 else BASE; bs = score(best, seeds, pool); print("base", bs, flush=True)
        for i in range(budget):
            cand = sample(rng, best)
            try: sc = score(cand, seeds, pool)
            except Exception as e: print("err", e); continue
            if sc[0] > bs[0]:
                best, bs = cand, sc; json.dump({"score": bs, "policy": best}, open(out, "w"), default=list)
                print(i, "NEW BEST", round(bs[0]), round(bs[1]), flush=True)
        print("final", bs)
