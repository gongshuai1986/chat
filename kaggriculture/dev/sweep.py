import sys, json
from harness import evaluate
base = "base_rita.py"
seeds = [1,2,3,4,5,6]
configs = {
 "base": {},
 "hands10": {"hands": 10},
 "hands12": {"hands": 12},
 "cow12sheep8": {"animal_target": {"COW":12,"SHEEP":8}, "build":[{"kind":"PASTURE","target":20,"share":0.5,"from_day":0,"until_day":20}]},
 "cow8sheep5_h10": {"hands":10, "animal_target": {"COW":8,"SHEEP":5}},
 "land3": {"land": 3},
 "feedfloat8": {"feed_float_days": 8},
 "feedfloat4": {"feed_float_days": 4},
 "batch4": {"animal_batch": 4},
 "strawb": {"crops":["WHEAT","STRAWBERRY"], "crop_share":{"WHEAT":0.5,"STRAWBERRY":0.5}, "plant_until":{"STRAWBERRY":12}},
 "melon": {"crops":["WHEAT","MELON"], "crop_share":{"WHEAT":0.6,"MELON":0.4}, "plant_until":{"MELON":14}, "fertilize_crops":["MELON"], "fert_stock":6},
 "collectfert": {"collect_fertilizer": True, "sell_order":["MILK","WOOL","FERTILIZER","WHEAT"]},
}
names = sys.argv[1:] or list(configs)
for n in names:
    r = evaluate(base, ["starter"], seeds, configs[n])["starter"]
    print(f"{n:16} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
