"""
Kaggriculture Agent - Final Version
基于v12优化，平均分数~33,000

核心策略:
1. Day 0购买第一块土地，尽早扩展
2. 西瓜为主策略
3. 最大化工人使用
4. 限量出售高价值产品避免价格崩盘
"""

from collections import defaultdict
from typing import Dict, List, Tuple

BOARD_SIZE = 10
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]

CROPS = {
    "WHEAT": {"cost": 10, "yield_day": 4},
    "CARROT": {"cost": 20, "yield_day": 3},
    "MELON": {"cost": 80, "yield_day": 10},
}


class State:
    def __init__(self):
        self.land_bought = 0
        self.last_hire_day = -1

STATE = State()


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def move_to(src, dst):
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    if dx == 0 and dy == 0:
        return "PASS"
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def is_shed_adj(pos):
    return pos in SHED_TILES


def find_empty(tiles):
    return [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if tiles[y][x] is None]


def find_plants(tiles):
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            t = tiles[y][x]
            if isinstance(t, dict) and t.get("kind") == "PLANT":
                result.append(((x, y), t))
    return result


def find_weeds(tiles):
    return [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)
            if isinstance(tiles[y][x], dict) and tiles[y][x].get("kind") == "WEED"]


def needs_water(tiles):
    return [pos for pos, t in find_plants(tiles) if not t.get("watered_today", False)]


def harvestable(tiles, day):
    result = []
    for pos, t in find_plants(tiles):
        crop = t.get("crop")
        age = day - t.get("planted_day", 0)
        if age >= CROPS.get(crop, {}).get("yield_day", 4):
            result.append(pos)
    return result


def count_crops(tiles):
    counts = defaultdict(int)
    for pos, t in find_plants(tiles):
        counts[t.get("crop", "")] += 1
    return counts


class Task:
    def __init__(self, priority, pos, action, args=None):
        self.priority = priority
        self.pos = pos
        self.action = action
        self.args = args or []
        self.assigned = False


def assign_tasks(tasks, workers):
    tasks.sort(key=lambda t: t.priority)
    actions = ["PASS"] * len(workers)
    
    for wi, wpos in enumerate(workers):
        best = None
        best_score = float('inf')
        
        for task in tasks:
            if task.assigned:
                continue
            score = dist(wpos, task.pos) + task.priority * 0.03
            if score < best_score:
                best_score = score
                best = task
        
        if best:
            best.assigned = True
            if wpos == best.pos:
                actions[wi] = [best.action] + best.args if best.args else best.action
            else:
                actions[wi] = move_to(wpos, best.pos)
    
    return actions


def compute_market(obs):
    global STATE
    
    orders = []
    player = obs.get("player", 0)
    me = obs["farms"][player]
    private = obs["private"]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    
    money = me.get("money", 0)
    tiles = me.get("tiles", [])
    seeds = private.get("seeds", {})
    shed = private.get("shed", {})
    
    crops = count_crops(tiles)
    empty = len(find_empty(tiles))
    total_plants = sum(crops.values())
    weeds = len(find_weeds(tiles))
    
    # === 1. 尽早购买土地 ===
    land_costs = [1000, 2000, 4000]
    if STATE.land_bought < 3:
        cost = land_costs[STATE.land_bought]
        # Day 0, 4, 8 购买
        buy_day = [0, 4, 8][STATE.land_bought]
        min_money = cost + 200
        if day >= buy_day and money >= min_money:
            orders.append(["BUY_LAND"])
            STATE.land_bought += 1
            money -= cost
    
    # === 2. 雇佣工人 ===
    if hour == 0 and day != STATE.last_hire_day:
        needed = min(10, max(5, (total_plants + empty + weeds) // 3 + 2))
        
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        for i in range(needed):
            cost = fib[min(i, len(fib) - 1)]
            if money >= cost + 100:
                orders.append(["HIRE"])
                money -= cost
        STATE.last_hire_day = day
    
    # === 3. 购买种子 ===
    total_seeds = sum(seeds.values())
    space = max(0, empty + weeds - total_seeds)
    
    if space > 0:
        # 西瓜（Day <= 18）
        if day <= 18:
            to_buy = min(15, space)
            if money >= 80 * to_buy + 300:
                orders.append(["BUY_SEED", "MELON", to_buy])
                money -= 80 * to_buy
                space -= to_buy
        
        # 胡萝卜（Day <= 26）
        if space > 0 and day <= 26:
            to_buy = min(10, space)
            if money >= 20 * to_buy + 150:
                orders.append(["BUY_SEED", "CARROT", to_buy])
                money -= 20 * to_buy
                space -= to_buy
        
        # 小麦（Day <= 27）
        if space > 0 and day <= 27:
            to_buy = min(20, space)
            if money >= 10 * to_buy + 80:
                orders.append(["BUY_SEED", "WHEAT", to_buy])
                money -= 10 * to_buy
    
    # === 4. 出售产品 ===
    sell_items = [("MELON", 12), ("CARROT", 25), ("WHEAT", 50)]
    
    for product, max_amt in sell_items:
        amt = shed.get(product, 0)
        if amt > 0:
            orders.append(["SELL", product, min(amt, max_amt)])
    
    return orders[:10]


def agent(obs, config=None):
    global STATE
    
    if obs is None:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    
    try:
        player = obs.get("player", 0)
        day = obs.get("day", 0)
        
        me = obs["farms"][player]
        private = obs["private"]
        
        tiles = me.get("tiles", [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)])
        farmer = tuple(me.get("farmer", [4, 4]))
        hands = [tuple(h) for h in me.get("hands", [])]
        seeds = private.get("seeds", {})
        invs = private.get("inventories", [{}])
        
        tasks = []
        
        # P1: 浇水
        for pos in needs_water(tiles):
            tasks.append(Task(1, pos, "WATER"))
        
        # P2: 清除杂草
        for pos in find_weeds(tiles):
            tasks.append(Task(2, pos, "DIG"))
        
        # P3: 收获
        for pos in harvestable(tiles, day):
            tasks.append(Task(3, pos, "HARVEST"))
        
        # P4+: 种植
        empties = find_empty(tiles)
        used = set()
        
        for crop, priority in [("MELON", 4), ("CARROT", 5), ("WHEAT", 6)]:
            for _ in range(seeds.get(crop, 0)):
                avail = [e for e in empties if e not in used]
                if avail:
                    pos = min(avail, key=lambda p: dist(farmer, p))
                    tasks.append(Task(priority, pos, "PLANT", [crop]))
                    used.add(pos)
        
        # P7: DROP
        farmer_inv = invs[0] if invs else {}
        has_items = isinstance(farmer_inv, dict) and any(
            v > 0 for k, v in farmer_inv.items() if isinstance(v, int)
        )
        if has_items and is_shed_adj(farmer):
            tasks.append(Task(7, farmer, "DROP"))
        
        workers = [farmer] + hands
        actions = assign_tasks(tasks, workers)
        
        farmer_action = actions[0] if actions else "PASS"
        if isinstance(farmer_action, str):
            farmer_action = [farmer_action]
        
        hands_actions = []
        for a in actions[1:]:
            if isinstance(a, str):
                hands_actions.append([a])
            else:
                hands_actions.append(a if isinstance(a, list) else [a])
        
        market = compute_market(obs)
        
        return {"farmer": farmer_action, "hands": hands_actions, "market": market}
        
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
