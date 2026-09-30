import sys
from harness import evaluate
seeds = [1,2,3,4,5,6]
def g(n=30, **k):
    d = dict(hands=8, animals=["GOOSE"], animal_target={"GOOSE": n}, animal_batch=4,
      build=[{"kind":"COOP","target":n,"share":0.6,"from_day":0,"until_day":20}],
      sell_order=["EGG","WHEAT"], sell_chunk=40, feed_float_days=2, animal_buffer=100,
      animal_floor=0, land=0, seed_stock=16, seed_batch=16, seed_buffer=100, animals_from_day=0, max_orders=12)
    d.update(k); return d
configs = {
 "a": g(),
 "a_ff4": g(feed_float_days=4),
 "a_b6": g(animal_batch=6),
 "a_h6": g(hands=6),
 "a_h10": g(hands=10),
 "a_l1": g(land=1, land_after_animals=8),
 "a_l2": g(land=2, land_after_animals=8),
 "a_s25": g(seed_stock=25, seed_batch=25),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
    r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
    print(f"{n:10} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
