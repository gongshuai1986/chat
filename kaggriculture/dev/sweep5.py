import sys
from harness import evaluate
seeds = [1,2,3,4,5,6]
CF = dict(collect_fertilizer=True, sell_order=["MILK","WOOL","FERTILIZER","WHEAT"])
configs = {
 "base": {},
 "cf": CF,
 "cf_s16": dict(CF, seed_stock=16, seed_batch=16),
 "cf_s24": dict(CF, seed_stock=24, seed_batch=24),
 "cf_s16_h10": dict(CF, seed_stock=16, seed_batch=16, hands=10),
 "cf_s16_pr": dict(CF, seed_stock=16, seed_batch=16, persistent_routing=True),
 "cf_s16_cz": dict(CF, seed_stock=16, seed_batch=16, cross_zone_penalty=6),
 "cf_s16_br": dict(CF, seed_stock=16, seed_batch=16, batched_restock=True),
 "cf_s16_ff10": dict(CF, seed_stock=16, seed_batch=16, feed_float_days=10),
 "cf_s16_a": dict(CF, seed_stock=16, seed_batch=16, animal_target={"COW":12,"SHEEP":8}, feed_float_days=10, build=[{"kind":"PASTURE","target":24,"share":0.5,"from_day":0,"until_day":20}]),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
    r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
    print(f"{n:12} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
