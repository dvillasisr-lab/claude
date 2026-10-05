import json, sys
T='single_line_text_field'; M='multi_line_text_field'; I='number_integer'; D='date'; B='boolean'; U='url'; DEC='number_decimal'
IMG='file_reference'; LT='list.single_line_text_field'
def ch(*v): return [{"name":"choices","value":json.dumps(list(v))}]
def f(key,typ,name=None,req=False,val=None):
    d={"key":key,"type":typ,"name":name or key.replace('_',' ').capitalize()}
    if req: d["required"]=True
    if val: d["validations"]=val
    return d
IMGV=[{"name":"file_type_options","value":json.dumps(["Image"])}]
def ref(gid): return [{"name":"metaobject_definition_id","value":gid}]
def batch1():
  return {
  "sponsor_tier":("Sponsor tier","name",[f("name",T,req=True),f("key",T,val=ch("title","pit","crew")),f("price",I,"Price (USD)"),f("tagline",T),f("benefits",LT),f("featured",B),f("status",T,val=ch("available","limited","soldout","hidden")),f("spots_left",I),f("order",I),f("updated",D)]),
  "season_stats":("Season stats","season",[f("season",I,req=True),f("competitions",I),f("competitions_note",T),f("exhibitions",I),f("wins",I),f("test_days",I),f("updated",D)]),
  "sponsor_stats":("Sponsor stats","social_text",[f("pulls_per_season",I),f("states",I),f("fans_per_pull",I),f("social_text",T),f("show_plus",B,"Show +"),f("estimated",B,"Show (est.)"),f("updated",D)]),
  "booking_option":("Booking option","name",[f("name",T,req=True),f("icon",T,val=ch("display","pull","meet","social")),f("text",M),f("needs",T),f("order",I)]),
  "crew_member":("Crew member","name",[f("name",T,req=True),f("role",T),f("group",T,val=ch("driver","team","pit_crew","mascot")),f("photo",IMG,val=IMGV),f("note",T),f("bio",M),f("order",I)]),
  "tractor_part":("Tractor part","name",[f("name",T,req=True),f("value",T),f("text",M),f("image",IMG,val=IMGV),f("image_position",T),f("pos_x",I,"X"),f("pos_y",I,"Y"),f("label_x",I),f("row",T,val=ch("top","bottom")),f("order",I)]),
  "size_chart":("Size chart","style",[f("style",T,req=True,val=ch("tee","long_sleeve","hoodie","crewneck","kids","cap","beanie")),f("unit",T),f("columns",LT),f("rows",LT),f("note",M)]),
  "faq_item":("FAQ item","question",[f("question",T,req=True),f("answer","rich_text_field"),f("category",T,val=ch("orders","shipping","returns","sizing","products","drops","payments","account","evil_list","sponsors","special_edition","tractor")),f("pages",LT),f("order",I)]),
  }
def batch2(tier, ):
  return {
  "album":("Album","event_name",[f("event_name",T,req=True),f("date",D),f("season",I),f("kind",T,val=ch("competition","exhibition","test")),f("city",T),f("league",T),f("cover",IMG,val=IMGV),f("photos","list.file_reference",val=IMGV),f("videos","list.url"),f("pit_log_url",U),f("order",I)]),
  "sponsor":("Sponsor","name",[f("name",T,req=True),f("logo",IMG,val=IMGV),f("tier","metaobject_reference",val=ref(tier)),f("shape",T,val=ch("round","square","wide")),f("link",U),f("active",B),f("order",I),f("season",I)]),
  "logo_placement":("Logo placement","name",[f("name",T,req=True),f("icon",T,val=ch("tractor","trailer","shirt","web","social","mic","pass")),f("description",M),f("packages","list.metaobject_reference",val=ref(tier)),f("package_details",LT),f("status",T,val=ch("active","hidden")),f("order",I),f("updated",D)]),
  "decal_zone":("Decal zone","name",[f("name",T,req=True),f("pos_x",I,"X"),f("pos_y",I,"Y"),f("label_x",I),f("row",T,val=ch("top","bottom")),f("size",T),f("tier","metaobject_reference",val=ref(tier)),f("status",T,val=ch("available","sold")),f("description",M),f("order",I),f("updated",D)]),
  }
def batch3(album):
  return {"pull_event":("Pull event","event_name",[f("event_name",T,req=True),f("date",D),f("start_time",T),f("season",I),f("calendar_label",T,val=[{"name":"max","value":"12"}]),f("city",T),f("league",T,val=ch("ntpa","badger_state","ihra_ppl","other")),f("type",T,val=ch("competition","exhibition")),f("status",T,val=ch("upcoming","done","cancelled","hidden")),f("result",T),f("place",I),f("full_pull",B),f("distance_ft",DEC),f("video",U),f("website",U),f("gallery_album","metaobject_reference",val=ref(album))])}
def mutation(defs, album_store=None):
  parts=[]; varsd={}
  for i,(t,(name,disp,fields)) in enumerate(defs.items()):
    d={"type":t,"name":name,"displayNameKey":disp,"access":{"storefront":"PUBLIC_READ"},"fieldDefinitions":fields}
    if t=="album": d["capabilities"]={"onlineStore":{"enabled":True,"data":{"urlHandle":"gallery-album"}},"renderable":{"enabled":True,"data":{"metaTitleKey":"event_name"}}}
    varsd[f"d{i}"]=d
    parts.append(f'  {t}: metaobjectDefinitionCreate(definition: $d{i}) {{ metaobjectDefinition {{ id type }} userErrors {{ field message code }} }}')
  head='mutation('+', '.join(f'$d{i}: MetaobjectDefinitionCreateInput!' for i in range(len(defs)))+') {\n'
  return head+'\n'.join(parts)+'\n}', varsd
if __name__=='__main__':
  b=sys.argv[1]
  if b=='1': q,v=mutation(batch1())
  elif b=='2': q,v=mutation(batch2(sys.argv[2]))
  else: q,v=mutation(batch3(sys.argv[2]))
  print(json.dumps({"query":q,"variables":v}))
