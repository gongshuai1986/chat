import sys
from cand import evaluate
POOL = ["ref/closer_cleo.py"]
seeds = list(range(1, 13))
C = {
 "base": {},
 "sells_first": {"_SELLS_FIRST": True},
 "wheat_always": {"_PROMOTE_IF_OPP_MONEY": {}},
 "shed60": {"_SHED_PRESSURE": 60},
 "fr2": {"_FRONT_RUN_HORIZON": 2},
 "fr_all": {"_FRONT_RUN_ITEMS": ("MELON","STRAWBERRY","MILK","WOOL","FERTILIZER","WHEAT")},
 "glut_hi": {"_GLUT_WEIGHT": {"MELON": 6.0, "STRAWBERRY": 4.0, "MILK": 4.0, "WOOL": 6.0}},
 "race2_sf": {"_RACE_WEIGHT": 2.0, "_SELLS_FIRST": True},
 "promote_fert_wheat": {"_PROMOTE": ('MILK','WOOL','STRAWBERRY','MELON','EGG','TOMATO','CARROT','FERTILIZER','WHEAT'), "_PROMOTE_IF_OPP_MONEY": {}},
}
for n in (sys.argv[1:] or C):
    w, tot, m, out = evaluate(C[n], seeds, pool=POOL)
    print(f"{n:20} mirror win {w}/{tot} margin {m:8.0f}", flush=True)
