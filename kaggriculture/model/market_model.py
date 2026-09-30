"""Exact market model of the Kaggriculture engine (prices, town demand) for plan evaluation."""
import math, itertools

PRODUCTS = ["WHEAT","CARROT","TOMATO","STRAWBERRY","MELON","EGG","MILK","WOOL","FERTILIZER"]
MP = {  # base, T, below_func, below_target, above_func, above_target
 "WHEAT": (25,400,"sqrt",0.80,"log",0.20), "CARROT": (35,450,"hinge",1.0,"sqrt",0.70),
 "TOMATO": (60,200,"hinge",0.40,"sqrt",0.60), "STRAWBERRY": (120,100,"sqrt",0.70,"linear",1.60),
 "MELON": (250,300,"log",0.20,"sq",3.60), "EGG": (50,332,"hinge",0.40,"log",0.20),
 "MILK": (160,122,"sqrt",0.60,"linear",1.60), "WOOL": (200,105,"log",0.20,"sq",3.20),
 "FERTILIZER": (100,200,"linear",0.40,"linear",0.40)}
I0 = 10000
SHOPS = {"BAKERY":["EGG","WHEAT"],"PIZZA_SHOP":["MILK","TOMATO","WHEAT"],"BRUNCH_SPOT":["EGG","WHEAT","STRAWBERRY"],
 "YARN_STORE":["WOOL"],"ICE_CREAM_SHOP":["STRAWBERRY","MILK","WHEAT"],"PET_CAFE":["CARROT"],
 "SMOOTHIE_SHOP":["STRAWBERRY","MILK"],"FARMERS_MARKET":["WHEAT","CARROT","TOMATO","STRAWBERRY"]}

def shape(f, x, T=None):
    x = max(0.0, x)
    if f == "linear": return x
    if f == "sq": return x*x
    if f == "sqrt": return math.sqrt(x)
    if f == "log": return math.log(1+x)
    if f == "hinge":
        u = x/T; return u + 8.0*max(0.0, u-1.0)**2

def price(item, inv):
    base, T, bf, bt, af, at = MP[item]
    if inv < I0:
        amp = bt*base/shape(bf, T, T); v = base + amp*shape(bf, I0-inv, T)
    else:
        amp = at*base/shape(af, T, T); v = base - amp*shape(af, inv-I0, T)
    return max(1, round(v))

def expected_daily_drain(item, instances):
    """Expected units/day consumed by `instances` randomly drawn shops + the town center."""
    per = 0.0
    for name, prods in SHOPS.items():
        if item in prods: per += 6 * (2 if len(prods) == 1 else 1) / len(SHOPS)
    center = 0 if item == "FERTILIZER" else 1
    return instances * per + center

def drain_total(item, d0=0, d1=30):
    return sum(expected_daily_drain(item, min(8, d // 3)) for d in range(d0, d1))

def sell_revenue(item, plan, other=None):
    """plan: units sold each day (list of 30). other: opponent units per day (same market).
    Inventory follows I0 + cumulative sales - cumulative drain; sales at price 1 don't add supply.
    Units within a day are sold one by one at the current price; drain applied once per day."""
    inv = float(I0); rev = 0.0
    for d in range(30):
        q = int(plan[d]); o = int(other[d]) if other else 0
        for k in range(q):
            p = price(item, inv); rev += p
            if p > 1: inv += 1
        for k in range(o):
            if price(item, inv) > 1: inv += 1
        inv -= expected_daily_drain(item, min(8, d // 3))
    return rev

if __name__ == "__main__":
    print(f"{'item':11} {'base':>5} {'drain/season':>12} {'free rev':>9}  price after +200 over-supply  daily drain @0/3/8 shops")
    for it in PRODUCTS:
        D = drain_total(it); base = MP[it][0]
        print(f"{it:11} {base:5} {D:12.0f} {base*D:9.0f}  {price(it, I0+200):>6}                         "
              f"{expected_daily_drain(it,0):.1f}/{expected_daily_drain(it,3):.1f}/{expected_daily_drain(it,8):.1f}")
