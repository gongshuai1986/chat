"""
Kaggriculture Agent v8 - 优化版本
基于v5改进：
1. 更激进的种子购买
2. 持续保持高种植密度
3. 更好的后期资源利用
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Optional

BOARD_SIZE = 10
TURNS_PER_DAY = 24
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]

CROPS = {
    "WHEAT": {"seed_cost": 10, "first_yield_day": 2, "max_yield_day": 4},
    "CARROT": {"seed_cost": 20, "first_yield_day": 2, "max_yield_day": 3},
    "MELON": {"seed_cost": 80, "first_yield_day": 10, "max_yield_day": 10},
}


class AgentState:
    def __init__(self):
        self.land_bought = 0
        self.last_hire_day = -1
        
STATE = AgentState()


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_move_direction(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> str:
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 0 and dy == 0:
        return "PASS"
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def is_tile_empty(tile) -> bool:
    return tile is None


def is_tile_plant(tile) -> bool:
    return isinstance(tile, dict) and tile.get("kind") == "PLANT"


def is_tile_weed(tile) -> bool:
    return isinstance(tile, dict) and tile.get("kind") == "WEED"


def find_plants_needing_water(tiles) -> List[Tuple[int, int]]:
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile = tiles[y][x]
            if is_tile_plant(tile) and not tile.get("watered_today", False):
                result.append((x, y))
    return result


def find_harvestable_plants(tiles, day: int) -> List[Tuple[int, int]]:
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile = tiles[y][x]
            if is_tile_plant(tile):
                crop = tile.get("crop")
                planted_day = tile.get("planted_day", 0)
                age = day - planted_day
                crop_info = CROPS.get(crop, {"max_yield_day": 4})
                if age >= crop_info["max_yield_day"]:
                    result.append((x, y))
    return result


def find_weeds(tiles) -> List[Tuple[int, int]]:
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if is_tile_weed(tiles[y][x]):
                result.append((x, y))
    return result


def find_empty_tiles(tiles) -> List[Tuple[int, int]]:
    result = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if is_tile_empty(tiles[y][x]):
                result.append((x, y))
    return result


def count_plants_by_crop(tiles) -> Dict[str, int]:
    counts = defaultdict(int)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile = tiles[y][x]
            if is_tile_plant(tile):
                counts[tile.get("crop", "")] += 1
    return counts


def is_shed_adjacent(pos: Tuple[int, int]) -> bool:
    return pos in SHED_TILES


def find_nearest(pos: Tuple[int, int], targets: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    if not targets:
        return None
    return min(targets, key=lambda t: manhattan_distance(pos, t))


class Task:
    def __init__(self, priority: int, pos: Tuple[int, int], action: str, args: List = None):
        self.priority = priority
        self.pos = pos
        self.action = action
        self.args = args or []
        self.assigned = False


def assign_tasks(tasks: List[Task], workers: List[Tuple[int, int]]) -> List:
    tasks.sort(key=lambda t: t.priority)
    actions = ["PASS"] * len(workers)
    
    for worker_idx, worker_pos in enumerate(workers):
        best_task = None
        best_score = float('inf')
        
        for task in tasks:
            if task.assigned:
                continue
            dist = manhattan_distance(worker_pos, task.pos)
            score = dist + task.priority * 0.1
            if score < best_score:
                best_score = score
                best_task = task
        
        if best_task:
            best_task.assigned = True
            if worker_pos == best_task.pos:
                if best_task.args:
                    actions[worker_idx] = [best_task.action] + best_task.args
                else:
                    actions[worker_idx] = best_task.action
            else:
                actions[worker_idx] = get_move_direction(worker_pos, best_task.pos)
    
    return actions


def compute_market_orders(obs: dict) -> List[List]:
    global STATE
    
    orders = []
    player = obs.get("player", 0)
    me = obs.get("farms", [{}, {}])[player]
    private = obs.get("private", {})
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    
    money = me.get("money", 0)
    tiles = me.get("tiles", [])
    seeds = private.get("seeds", {})
    shed = private.get("shed", {})
    
    crop_counts = count_plants_by_crop(tiles)
    empty_count = len(find_empty_tiles(tiles))
    total_plants = sum(crop_counts.values())
    
    # === 购买土地 ===
    unlocked = len(me.get("unlocked_quadrants", ["NW"]))
    land_costs = [1000, 2000, 4000]
    
    if STATE.land_bought < 3:
        cost = land_costs[STATE.land_bought]
        threshold_day = 4 + STATE.land_bought * 4
        if day >= threshold_day and money >= cost + 1500:
            orders.append(["BUY_LAND"])
            STATE.land_bought += 1
            money -= cost
    
    # === 雇佣工人 ===
    if hour == 0 and day != STATE.last_hire_day:
        needed = min(10, max(3, total_plants // 3 + 2))
        
        fib = [1, 1, 2, 3, 5, 8, 13, 21]
        for i in range(needed):
            cost = fib[min(i, len(fib) - 1)]
            if money >= cost + 300:
                orders.append(["HIRE"])
                money -= cost
        STATE.last_hire_day = day
    
    # === 购买种子（持续保持农场满载）===
    wheat_seeds = seeds.get("WHEAT", 0)
    carrot_seeds = seeds.get("CARROT", 0)
    melon_seeds = seeds.get("MELON", 0)
    total_seeds = wheat_seeds + carrot_seeds + melon_seeds
    
    # 目标：让空地数量接近0
    need_more = empty_count > total_seeds
    
    if need_more:
        space_to_fill = empty_count - total_seeds
        
        # 西瓜 (day <= 18)
        if day <= 18 and money >= 300:
            to_buy = min(8, space_to_fill)
            cost = 80 * to_buy
            if money >= cost + 400:
                orders.append(["BUY_SEED", "MELON", to_buy])
                money -= cost
                space_to_fill -= to_buy
        
        # 胡萝卜 (day <= 26)
        if space_to_fill > 0 and day <= 26 and money >= 150:
            to_buy = min(6, space_to_fill)
            cost = 20 * to_buy
            if money >= cost + 200:
                orders.append(["BUY_SEED", "CARROT", to_buy])
                money -= cost
                space_to_fill -= to_buy
        
        # 小麦（始终可买，day <= 27）
        if space_to_fill > 0 and day <= 27 and money >= 80:
            to_buy = min(12, space_to_fill)
            cost = 10 * to_buy
            if money >= cost + 100:
                orders.append(["BUY_SEED", "WHEAT", to_buy])
                money -= cost
    
    # === 出售产品 ===
    sell_items = [
        ("MELON", 10),
        ("CARROT", 20),
        ("WHEAT", 30),
    ]
    
    for product, max_sell in sell_items:
        amount = shed.get(product, 0)
        if amount > 0:
            sell_amt = min(amount, max_sell)
            orders.append(["SELL", product, sell_amt])
    
    return orders[:10]


def agent(obs: dict, config: dict = None) -> dict:
    global STATE
    
    if obs is None:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    
    try:
        player = obs.get("player", 0)
        day = obs.get("day", 0)
        
        me = obs.get("farms", [{}, {}])[player]
        private = obs.get("private", {})
        
        tiles = me.get("tiles", [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)])
        farmer_pos = tuple(me.get("farmer", [4, 4]))
        hands_pos = [tuple(h) for h in me.get("hands", [])]
        seeds = private.get("seeds", {})
        inventories = private.get("inventories", [{}])
        
        tasks = []
        
        # P1: 浇水
        for pos in find_plants_needing_water(tiles):
            tasks.append(Task(1, pos, "WATER"))
        
        # P2: 清除杂草
        for pos in find_weeds(tiles):
            tasks.append(Task(2, pos, "DIG"))
        
        # P3: 收获
        for pos in find_harvestable_plants(tiles, day):
            tasks.append(Task(3, pos, "HARVEST"))
        
        # P4-6: 种植
        empty_tiles = find_empty_tiles(tiles)
        used_tiles = set()
        
        melon_seeds = seeds.get("MELON", 0)
        for _ in range(min(melon_seeds, len(empty_tiles))):
            available = [t for t in empty_tiles if t not in used_tiles]
            if available:
                pos = find_nearest(farmer_pos, available)
                if pos:
                    tasks.append(Task(4, pos, "PLANT", ["MELON"]))
                    used_tiles.add(pos)
        
        carrot_seeds = seeds.get("CARROT", 0)
        for _ in range(min(carrot_seeds, len(empty_tiles) - len(used_tiles))):
            available = [t for t in empty_tiles if t not in used_tiles]
            if available:
                pos = find_nearest(farmer_pos, available)
                if pos:
                    tasks.append(Task(5, pos, "PLANT", ["CARROT"]))
                    used_tiles.add(pos)
        
        wheat_seeds = seeds.get("WHEAT", 0)
        for _ in range(min(wheat_seeds, len(empty_tiles) - len(used_tiles))):
            available = [t for t in empty_tiles if t not in used_tiles]
            if available:
                pos = find_nearest(farmer_pos, available)
                if pos:
                    tasks.append(Task(6, pos, "PLANT", ["WHEAT"]))
                    used_tiles.add(pos)
        
        # P7: DROP
        farmer_inv = inventories[0] if inventories else {}
        has_items = isinstance(farmer_inv, dict) and any(
            v > 0 for k, v in farmer_inv.items() if isinstance(v, int)
        )
        if has_items and is_shed_adjacent(farmer_pos):
            tasks.append(Task(7, farmer_pos, "DROP"))
        
        workers = [farmer_pos] + hands_pos
        actions = assign_tasks(tasks, workers)
        
        farmer_action = actions[0] if actions else "PASS"
        if isinstance(farmer_action, str):
            farmer_action = [farmer_action]
        
        hands_actions = []
        for action in actions[1:]:
            if isinstance(action, str):
                hands_actions.append([action])
            else:
                hands_actions.append(action if isinstance(action, list) else [action])
        
        market_orders = compute_market_orders(obs)
        
        return {
            "farmer": farmer_action,
            "hands": hands_actions,
            "market": market_orders
        }
        
    except Exception as e:
        return {"farmer": ["PASS"], "hands": [], "market": []}
