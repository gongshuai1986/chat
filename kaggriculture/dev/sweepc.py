import sys, json
from cand import evaluate
seeds = list(range(1, 7))
C = {
 "sort_gross": {"_SORT_KEY": "gross"},
 "sort_unit": {"_SORT_KEY": "unit"},
 "sells_first": {"_SELLS_FIRST": True},
 "race1": {"_RACE_WEIGHT": 1.0},
 "race3": {"_RACE_WEIGHT": 3.0},
 "fr0": {"_FRONT_RUN_HORIZON": 0},
 "fr3": {"_FRONT_RUN_HORIZON": 3},
 "reserve25": {"_RESERVE": {"MELON":0.25,"MILK":0.25,"WOOL":0.25,"STRAWBERRY":0.25}},
 "shed70": {"_SHED_PRESSURE": 70},
 "wheat_always": {"_PROMOTE_IF_OPP_MONEY": {}},
 "promote_all": {"_PROMOTE": ()},
}
names = sys.argv[1:] or list(C)
for n in names:
    w, tot, m, out = evaluate(C[n], seeds)
    print(f"{n:14} win {w}/{tot} margin {m:8.0f}", {k: v[0] for k, v in out.items()}, flush=True)
