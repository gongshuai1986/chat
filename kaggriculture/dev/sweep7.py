import sys
from harness import evaluate
seeds = [1,2,3,4,5,6]
B = dict(collect_fertilizer=True, seed_stock=16, seed_batch=16, feed_float_days=8, persistent_routing=True, batched_restock=True, hands=9)
def mix(g, c, s, sell=None, **k):
    d = dict(B, animals=["GOOSE","COW","SHEEP"], animal_target={"GOOSE":g,"COW":c,"SHEEP":s},
      build=[{"kind":"COOP","target":g,"share":0.3,"from_day":0,"until_day":20},{"kind":"PASTURE","target":c+s,"share":0.4,"from_day":0,"until_day":20}],
      sell_order=["EGG","MILK","WOOL","FERTILIZER","WHEAT"], sell_chunk=40)
    d.update(k); return d
configs = {
 "ref": dict(B, sell_order=["MILK","WOOL","FERTILIZER","WHEAT"]),
 "g0": mix(0,10,6),
 "g8": mix(8,10,6),
 "g16": mix(16,10,6),
 "g16c6s3": mix(16,6,3),
 "g24c0s0": mix(24,0,0),
 "g12c4s4": mix(12,4,4),
}
if __name__=="__main__":
  for n in (sys.argv[1:] or configs):
    r = evaluate("base_rita.py", ["starter"], seeds, configs[n])["starter"]
    print(f"{n:12} mine={r[0]:9.0f} opp={r[1]:6.0f} wins={r[2]}/{r[3]}", flush=True)
