import json, sys, pprint
src = open("plan_agent.py").read()
pol = json.load(open(sys.argv[1]))["policy"]
start = src.index("POLICY = {"); end = src.index("# ---------------------------------------------------------------------------\n# Shared action scheduler")
hdr = "POLICY = " + pprint.pformat(pol, width=100, sort_dicts=False) + "\n\n\n"
open(sys.argv[2], "w").write(src[:start] + hdr + src[end:])
