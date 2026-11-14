import json
PRE=3/25
import re
def H(text,t,g=()):
    text=re.sub(r"([A-Za-z]+) (?=[A-Za-z])",lambda m:m.group(1)+"\u00a0",text)   # an English term stays one word (RTL line would flip it)
    return [{"w":x,"t":t,"e":t,"g":(k in g)} for k,x in enumerate(text.split(" "))]
def KB(*rows):
    t0=min(ks[0] for _,ks in rows); out=[]
    for ri,(text,ks) in enumerate(rows):
        xs=text.split(" "); assert len(xs)==len(ks),text
        for x,k in zip(xs,ks): out.append({"w":x,"t":t0,"e":t0,"g":False,"k":k,"r":ri})
    return out
def card(title,rows,start,end,top=1000):
    L=[H(title,start+PRE,(0,1,2))]
    for text,t in rows: L.append(H(text,t))
    return {"type":"list","start":round(start,3),"end":round(end,3),"top":top,"num":"","lines":L}
o=lambda txt,t:{"w":txt,"t":t}
def ins(O,C,items,y0):
    return {"open":O,"close":C,"end":round(C+0.32,2),"ck":0.2,"cy1":0.18,"fa":0.2,"fb":0.3,"cy":900,"sc":0.66,"dx":50,"dy":310,
            "y0":y0,"y1":y0,"align":1,"itemH":176,"items":items}
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
KEY=[0.0,0.12,0.27,0.45,0.59,0.835,1.125,1.415]   # keyboard clicks in keaboard.MP3 from 0.645 s (segment from 0.6, peak 0.045)
def write(d,data,INS,fx):
    json.dump(data,open(f"{d}/data.json","w"),ensure_ascii=False)
    json.dump(INS,open(f"{d}/ins.json","w"),ensure_ascii=False)
    open(f"{d}/ins_page.html","w").write(open("ins_tpl.html").read().replace("DATA",json.dumps(INS,ensure_ascii=False)))
    open(f"{d}/sfx.txt","w").write("\n".join(fx)+"\n")
