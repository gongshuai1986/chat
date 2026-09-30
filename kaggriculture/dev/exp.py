import sys, json, copy, multiprocessing as mp
import search
base = json.load(open("/tmp/best_plan4.json"))["policy"]
def P(**k):
    p = copy.deepcopy(base); p.update(k); return p
FF = {"MILK": .8, "WOOL": .8, "STRAWBERRY": .8, "EGG": .7, "FERTILIZER": .6, "TOMATO": .8, "CARROT": .8, "WHEAT": .0}
def model(cows, sheep, geese, **extra):
    a = ["COW", "SHEEP", "GOOSE"] if geese else ["COW", "SHEEP"]
    d = dict(animals=a, animal_target={"COW": cows, "SHEEP": sheep, "GOOSE": geese},
             build=[{"kind":"PASTURE","target":cows+sheep+1,"share":0.4,"from_day":0,"until_day":20}] + ([{"kind":"COOP","target":geese,"share":0.45,"from_day":0,"until_day":20}] if geese else []),
             sell_order=["EGG","MILK","WOOL","STRAWBERRY","FERTILIZER","TOMATO","CARROT","WHEAT"], max_sell_orders=8, floor_frac=FF,
             collect_fertilizer=True)
    d.update(extra); return d
C = {
 "base4": {},
 "floor_only": dict(floor_frac=FF, sell_order=["EGG","MILK","WOOL","FERTILIZER","WHEAT"], max_sell_orders=6),
 "m_6_3_0": model(6,3,0),
 "m_6_3_12": model(6,3,12, feed_float_days=8),
 "m_6_3_20": model(6,3,20, feed_float_days=8),
 "m_6_3_12_land": model(6,3,12, feed_float_days=8, land_days=[4,9,14], land_buffer=300),
 "m_6_3_12_straw": model(6,3,12, feed_float_days=8, crops=["WHEAT","STRAWBERRY"], crop_share={"WHEAT":0.5,"STRAWBERRY":0.5}, plant_until={"STRAWBERRY":12,"WHEAT":25}, land_days=[4,9,14], land_buffer=300),
}
if __name__ == "__main__":
    seeds = [1,2,3,4,5,6,7,8]
    with mp.Pool(4) as pool:
        for n in (sys.argv[1:] or C):
            pol = copy.deepcopy(base) if n == "base4" else P(**C[n])
            m, mn = search.score(pol, seeds, pool)
            print(f"{n:16} blended {m:8.0f} min {mn:8.0f}", flush=True)
