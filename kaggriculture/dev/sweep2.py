import sys, json
from harness import evaluate
seeds = [1,2,3,4,5,6]
def P(**k): return k
goose = lambda n, batch=4, hands=10, coops=None, **extra: dict(
    hands=hands, animals=["GOOSE"], animal_target={"GOOSE": n}, animal_batch=batch,
    build=[{"kind":"COOP","target":coops or n,"share":0.6,"from_day":0,"until_day":20}],
    sell_order=["EGG","WHEAT"], sell_chunk=40, **extra)
configs = {
 "g20": goose(20),
 "g30": goose(30),
 "g40": goose(40),
 "g30_h12": goose(30, hands=12),
 "g30_l3": goose(30, land=3),
 "g30_fl6": goose(30, feed_float_days=6),
 "g30_fl3": goose(30, feed_float_days=3),
 "g30_batch8": goose(30, batch=8, feed_float_days=6),
 "g30_nocare": goose(30, care=False),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
      r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
      print(f"{n:16} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
