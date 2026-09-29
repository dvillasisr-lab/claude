import ringsearch as R
res=[]
for r in range(150,186,5):
  for cx in range(540,720,10):
    for cy in range(360,440,5):
      e=R.evaluate(cx,cy,r)
      if e['logo']>=26 and e['low']<=575 and e['kick']>=40 and e['title']>=60 and e['minrun']>=60:
        g,_=R.graze(cx,cy,r)
        if g<=12: res.append((r,cx,cy,g,e))
res.sort(key=lambda t:(-t[0],t[3],-t[4]['frac']))
for t in res[:30]: print(t)
print(len(res))
