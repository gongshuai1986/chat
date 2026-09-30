import sys
from harness import evaluate
seeds = [1,2,3,4,5,6]
def w(**k):
    d = dict(hands=10, animals=[], animal_target={}, build=[], care=False, crops=["WHEAT"], crop_share={"WHEAT":1.0},
      sell_order=["WHEAT"], sell_chunk=200, feed_float_days=0, land=3, land_after_animals=0, land_buffer=300,
      seed_stock=25, seed_batch=25, seed_buffer=100, max_orders=12, shed_pressure=60, invest_until_day=25, plant_until_day=26, liquidate_from_day=27, max_sell_orders=4)
    d.update(k); return d
configs = {
 "w_l0_h8": w(land=0, hands=8),
 "w_l1_h8": w(land=1, hands=8),
 "w_l2_h10": w(land=2, hands=10),
 "w_l3_h10": w(land=3, hands=10),
 "w_l3_h12": w(land=3, hands=12),
 "w_l3_h14": w(land=3, hands=14),
 "w_l3_h10_pr": w(land=3, hands=10, persistent_routing=True),
 "w_l3_h10_cz": w(land=3, hands=10, cross_zone_penalty=6),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
    r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
    print(f"{n:12} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
