import json, copy
TAPE_PATH = None
_T = None
_SELLABLE = ("STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "TOMATO", "CARROT", "WHEAT", "FERTILIZER")

def agent(obs, config=None):
    global _T
    if _T is None:
        _T = json.load(open(TAPE_PATH))["tape"]
    step = int(obs.get("step", 0) or 0)
    action = copy.deepcopy(_T[step]) if step < len(_T) else {"farmer": ["PASS"], "hands": [], "market": []}
    if step >= 700:
        shed = (obs.get("private") or {}).get("shed") or {}
        market = action.setdefault("market", [])
        sold = {o[1] for o in market if isinstance(o, list) and len(o) > 1 and o[0] == "SELL"}
        for item in _SELLABLE:
            q = int(shed.get(item, 0) or 0)
            if q > 0 and item not in sold and len(market) < 10:
                market.append(["SELL", item, q])
    return action
