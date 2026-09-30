import sys
from harness import evaluate
seeds = [1,2,3,4,5,6]
B = dict(collect_fertilizer=True, sell_order=["MILK","WOOL","FERTILIZER","WHEAT"], seed_stock=16, seed_batch=16, feed_float_days=10)
configs = {
 "B": B,
 "B_pr_br": dict(B, persistent_routing=True, batched_restock=True),
 "B_pr_br_cz": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6),
 "B_pr_cz": dict(B, persistent_routing=True, cross_zone_penalty=6),
 "B_all_ff8": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6, feed_float_days=8),
 "B_all_ff12": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6, feed_float_days=12),
 "B_all_h9": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6, hands=9),
 "B_all_h7": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6, hands=7),
 "B_all_drop": dict(B, persistent_routing=True, batched_restock=True, cross_zone_penalty=6, drop_threshold=8),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
    r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
    print(f"{n:12} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
