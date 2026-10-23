NAVY='ColorValue("#202054")'; GREY='ColorValue("#616066")'; LIGHT='ColorValue("#EEEEF5")'
out=[]
def fx(v):
    v=str(v)
    if "\n" in v or ": " in v or " #" in v or v.startswith("#"):
        return "|-\n" + "\n".join("  " + l for l in ("=" + v).split("\n"))
    return "=" + v
def ctrl(name, typ, props, indent=0, variant=None, children=None):
    p=" "*indent
    s=[f"{p}- {name}:", f"{p}    Control: {typ}"]
    if variant: s.append(f"{p}    Variant: {variant}")
    s.append(f"{p}    Properties:")
    for k,v in props.items():
        val=fx(v)
        if val.startswith("|-"):
            lines=val.split("\n")
            s.append(f"{p}      {k}: |-")
            for l in lines[1:]:
                s.append(f"{p}      {l}")
        else:
            s.append(f"{p}      {k}: {val}")
    if children:
        s.append(f"{p}    Children:")
        for c in children: s.append(c)
    return "\n".join(s)
def A(x): out.append(x)
R={"RadiusTopLeft":"8","RadiusTopRight":"8","RadiusBottomLeft":"8","RadiusBottomRight":"8"}
def pill(r=18): return {"RadiusTopLeft":str(r),"RadiusTopRight":str(r),"RadiusBottomLeft":str(r),"RadiusBottomRight":str(r)}
def label(name, text, x, y, w, h, size=11, color=NAVY, bold=False, visible=None, extra=None):
    p={"Text":text,"X":x,"Y":y,"Width":w,"Height":h,"Size":str(size),"Color":color}
    if bold: p["FontWeight"]="FontWeight.Bold"
    if visible: p["Visible"]=visible
    if extra: p.update(extra)
    return ctrl(name,"Label@2.5.1",p)
def button(name, text, x, y, w, h, onselect, fill=NAVY, color="Color.White", visible=None, size=11, extra=None, r=18):
    p={"Text":text,"X":x,"Y":y,"Width":w,"Height":h,"Size":str(size),"Fill":fill,"Color":color,
       "HoverFill":"ColorValue(\"#3B3B8F\")" if fill==NAVY else "ColorValue(\"#C9C9D6\")","FontWeight":"FontWeight.Semibold","BorderThickness":"0","OnSelect":onselect}
    p.update(pill(r))
    if visible: p["Visible"]=visible
    if extra: p.update(extra)
    return ctrl(name,"Classic/Button@2.2.0",p)
def textinput(name, default, hint, x, y, w, h, visible=None, multi=False):
    p={"Default":default,"HintText":'"' + hint + '"',"X":x,"Y":y,"Width":w,"Height":h,"Size":"11","BorderColor":'ColorValue("#C9C9D6")'}
    p.update(R)
    if multi: p["Mode"]="TextMode.MultiLine"
    if visible: p["Visible"]=visible
    return ctrl(name,"Classic/TextInput@2.3.2",p)
def chips(name, items, x, y, w, h, selected, onselect, visible, wrap=2, tsize=30):
    btn=ctrl("btn"+name,"Classic/Button@2.2.0",{
        "Text":"ThisItem.Value","X":"0","Y":"2","Width":"Parent.TemplateWidth - 6","Height":str(tsize-6),"Size":"9",
        "Fill":f"If({selected}, {NAVY}, {LIGHT})","HoverFill":'ColorValue("#C9C9D6")',
        "Color":f"If({selected}, Color.White, {NAVY})","BorderThickness":"0","OnSelect":onselect, **pill(12)}, indent=6)
    return ctrl("gal"+name,"Gallery@2.15.0",{"Items":items,"X":x,"Y":y,"Width":w,"Height":h,"WrapCount":str(wrap),
        "TemplateSize":str(tsize),"TemplatePadding":"0","ShowScrollbar":"false","Visible":visible},variant="Vertical",children=[btn])

