from market_model import *
START = {"WHEAT":2,"CARROT":2,"TOMATO":8,"STRAWBERRY":10,"MELON":10,"EGG":4,"MILK":8,"WOOL":6}
def even_plan(Q, d0):
    days = list(range(d0, 30)); plan = [0]*30
    for i in range(Q): plan[days[i % len(days)]] += 1
    return plan
def best(item, shared):
    d0 = START[item]; bestQ, bestR = 0, 0.0
    for Q in range(0, 1200, 4):
        plan = even_plan(Q, d0)
        R = sell_revenue(item, plan, plan if shared else None)
        if R > bestR: bestQ, bestR = Q, R
    return bestQ, bestR
tot_a = tot_s = 0
print(f"{'item':11} {'alone: Q*':>9} {'rev':>8}   {'shared: Q*':>10} {'rev(each)':>9}")
for it in START:
    qa, ra = best(it, False); qs, rs = best(it, True)
    tot_a += ra; tot_s += rs
    print(f"{it:11} {qa:9} {ra:8.0f}   {qs:10} {rs:9.0f}")
print(f"{'TOTAL':11} {'':9} {tot_a:8.0f}   {'':10} {tot_s:9.0f}")
