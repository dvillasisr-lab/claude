import json,sys,os
D=os.path.dirname(__file__)+'/seed/'
def build(items):
  parts=[];v={}
  for i,(t,o) in enumerate(items):
    v[f"i{i}"]={"fields":o["fields"]}
    parts.append(f'  a{i}: metaobjectUpsert(handle: {{type: "{t}", handle: "{o["handle"]}"}}, metaobject: $i{i}) {{ metaobject {{ handle }} userErrors {{ field message }} }}')
  q="mutation("+", ".join(f"$i{j}: MetaobjectUpsertInput!" for j in range(len(items)))+") {\n"+"\n".join(parts)+"\n}"
  return q,v
mode=sys.argv[1]
if mode=='small':
  items=[]
  for t in ['sponsor_tier','sponsor_stats','season_stats','crew_member','booking_option','tractor_part','logo_placement','decal_zone','pull_event']:
    for o in json.load(open(D+t+'.json')): items.append((t,o))
else:
  a,b=map(int,mode.split(':'))
  items=[('faq_item',o) for o in json.load(open(D+'faq_item.json'))[a:b]]
q,v=build(items)
open('/tmp/claude-0/-home-user-claude/e3596acf-3a72-571c-8bcd-cf17bcda8b4d/scratchpad/up_q.txt','w').write(q)
open('/tmp/claude-0/-home-user-claude/e3596acf-3a72-571c-8bcd-cf17bcda8b4d/scratchpad/up_v.json','w').write(json.dumps(v,ensure_ascii=False))
print(len(items), len(q), len(json.dumps(v,ensure_ascii=False)))
