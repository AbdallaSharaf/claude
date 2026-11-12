import json,sys
D=json.load(open(sys.argv[1])); C=D["close"]
if "lines" in D["items"][0]: last=max((w for it in D["items"] for L in it["lines"] for w in L),key=lambda w:w["t"]); lt,lw=last["t"],last["w"]
else: lt,lw=D["items"][-1]["t"],"item"
v=C-(lt-0.12+0.15); print("insert last word",lw,"readable",round(v,2),"s before close",("OK" if v>=0.8 else "TOO SHORT"))
