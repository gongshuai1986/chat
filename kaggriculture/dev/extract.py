import json, sys, os
def extract(f, outdir="tapes"):
    d = json.load(open(f)); ep = d["info"]["EpisodeId"]; names = d["info"]["TeamNames"]
    out = []
    for p in (0, 1):
        tape = [d["steps"][t+1][p]["action"] for t in range(len(d["steps"]) - 1)]
        path = f"{outdir}/{ep}_{p}.json"
        json.dump({"team": names[p], "reward": d["rewards"][p], "opp": names[1-p], "opp_reward": d["rewards"][1-p], "episode": ep, "tape": tape}, open(path, "w"), separators=(",", ":"))
        out.append((path, names[p], d["rewards"][p], names[1-p], d["rewards"][1-p]))
    return out
if __name__ == "__main__":
    for f in sys.argv[1:]:
        for r in extract(f): print(r)
