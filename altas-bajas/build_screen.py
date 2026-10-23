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

NEW='varTipo = "New hire"'; TERM='varTipo = "Termination"'; CHG='varTipo = "Change"'
FORM='varModo = "new"'
X0="400"; W="(Parent.Width - 420)"; CW=f"({W} - 40) / 3"
def cx(i): return f"{X0} + ({CW} + 20) * {i}"

DEPTS='["AC - Accounting", "AM - Administration", "CS - Customer Service", "EN - Engineering", "HR - Human Resources", "IT - Information Technology", "MT - Maintenance", "OP - Operations", "PC - Production Control", "PD - Production", "QA - Quality", "SA - Sales", "SR - Shipping/Receiving"]'
COMPS='["Sussek Machine Company", "Sussek De Mexico", "Sussek Metalworking Solutions", "Nelson Numeric Inc.", "Reynold\'s Machine Company"]'
LOCS='["Waterloo", "New Berlin", "Mexico", "Remote"]'
EQUIP='["Laptop", "Desktop", "Monitor", "Cell phone", "Desk phone", "Badge / keys", "Email & Teams", "VPN", "ERP access", "Shop floor terminal"]'

# ---------- header ----------
A(ctrl("recHeadR","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.Width","Height":"64","Fill":NAVY}))
A(label("lblTitleR",'"People Requests"',"24","0","300","64",16,"Color.White",True))
A(label("lblITCapR",'"Sends to IT:"',"Parent.Width - 560","0","100","64",10,'ColorValue("#C9C9D6")'))
A(label("lblITR",'"CORREO_DE_IT@sussek.com"',"Parent.Width - 465","0","260","64",11,"Color.White",True))
A(button("btnNewR",'"+ New request"',"Parent.Width - 190","14","170","36",
 '''Set(varModo, "new"); Set(varTipo, "New hire"); Set(varPick, "");
Set(varEmp, {N: "", C: ""}); Set(varMgr, {N: "", C: ""}); Set(varMgrAntes, {N: "", C: ""}); Set(varBackup, {N: "", C: ""}); Set(varReasign, {N: "", C: ""}); Set(varMbx, {N: "", C: ""});
Set(varF, {Puesto: "", Depto: "", Empresa: "", Loc: "", Desc: "", Scope: "", Skills: ""});
Set(varDept, ""); Set(varComp, ""); Set(varLoc, ""); Clear(colEquip);
Set(varLista, ""); Reset(txtNombreR); Reset(txtFechaR); Reset(txtPuestoR); Reset(txtDescR); Reset(txtScopeR); Reset(txtSkillsR); Reset(txtAccesosR); Reset(txtNotasR); Reset(txtAutoR)''',
 fill="Color.White", color=NAVY))

# ---------- left list ----------
A(ctrl("recLeftR","Rectangle@2.3.0",{"X":"0","Y":"64","Width":"380","Height":"Parent.Height - 64","Fill":'ColorValue("#F6F6FA")'}))
A(ctrl("galTabsR","Gallery@2.15.0",{"Items":'["All", "Open", "New hire", "Termination", "Change"]',"X":"12","Y":"76","Width":"356","Height":"64",
  "WrapCount":"3","TemplateSize":"32","TemplatePadding":"0","ShowScrollbar":"false"},variant="Vertical",children=[
  ctrl("btnTabR","Classic/Button@2.2.0",{"Text":"ThisItem.Value","X":"0","Y":"2","Width":"Parent.TemplateWidth - 6","Height":"26","Size":"9",
   "Fill":f'If(Coalesce(varFiltroT, "All") = ThisItem.Value, {NAVY}, Color.White)',"Color":f'If(Coalesce(varFiltroT, "All") = ThisItem.Value, Color.White, {NAVY})',
   "HoverFill":'ColorValue("#C9C9D6")',"BorderThickness":"0","OnSelect":"Set(varFiltroT, ThisItem.Value)",**pill(13)},indent=6)]))
rowkids=[
 ctrl("recRowR","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.TemplateWidth","Height":"Parent.TemplateHeight - 6","Fill":'If(!IsBlank(varSel) && varSel.ID = ThisItem.ID, ColorValue("#E2E2EE"), Color.White)',
   "BorderColor":'ColorValue("#E3E3E3")',"BorderThickness":"1","OnSelect":'Set(varSel, ThisItem); Set(varModo, "view")'},indent=6),
 ctrl("lblBadgeR","Label@2.5.1",{"Text":"ThisItem.RequestType","X":"10","Y":"8","Width":"96","Height":"22","Size":"8","Align":"Align.Center","FontWeight":"FontWeight.Bold","Color":"Color.White",
   "Fill":'Switch(ThisItem.RequestType, "New hire", ColorValue("#1E7B34"), "Termination", ColorValue("#B3261E"), ColorValue("#3E7CB1"))'},indent=6),
 ctrl("lblStatusR","Label@2.5.1",{"Text":"ThisItem.Status","X":"Parent.TemplateWidth - 110","Y":"8","Width":"100","Height":"22","Size":"8","Align":"Align.Right",
   "Color":'If(ThisItem.Status = "Done", ColorValue("#1E7B34"), ColorValue("#B36B00"))',"FontWeight":"FontWeight.Semibold"},indent=6),
 ctrl("lblNameRowR","Label@2.5.1",{"Text":"ThisItem.Title","X":"10","Y":"32","Width":"Parent.TemplateWidth - 20","Height":"24","Size":"11","FontWeight":"FontWeight.Bold","Color":NAVY},indent=6),
 ctrl("lblDateRowR","Label@2.5.1",{"Text":'Switch(ThisItem.RequestType, "New hire", "Start ", "Termination", "Last day ", "Effective ") & Text(ThisItem.EffectiveDate, "mmm d, yyyy", "en-US") & "  ·  " & Coalesce(ThisItem.JobTitle, ThisItem.EmployeeEmail)',
   "X":"10","Y":"54","Width":"Parent.TemplateWidth - 20","Height":"22","Size":"9","Color":GREY},indent=6)]
A(ctrl("galReqR","Gallery@2.15.0",{"Items":'Sort(Filter(PeopleRequests, Coalesce(varFiltroT, "All") = "All" || (varFiltroT = "Open" && Status <> "Done") || RequestType = varFiltroT), Created, SortOrder.Descending)',
  "X":"12","Y":"146","Width":"356","Height":"Parent.Height - 156","TemplateSize":"88","TemplatePadding":"0","ShowScrollbar":"true"},variant="Vertical",children=rowkids))

# ---------- empty state ----------
A(label("lblEmptyR",'"Select a request on the left, or press + New request."',X0,"300",W,"40",12,GREY,False,'varModo <> "new" && varModo <> "view"',{"Align":"Align.Center"}))

# ---------- form: type selector ----------
A(label("lblFormTitleR",'"New request"',X0,"72",'300',"40",15,NAVY,True,FORM))
A(ctrl("galTipoR","Gallery@2.15.0",{"Items":'["New hire", "Termination", "Change"]',"X":f"{X0} + 200","Y":"76","Width":"480","Height":"36","WrapCount":"3","TemplateSize":"36","TemplatePadding":"0","ShowScrollbar":"false","Visible":FORM},variant="Vertical",children=[
  ctrl("btnTipoR","Classic/Button@2.2.0",{"Text":"ThisItem.Value","X":"0","Y":"0","Width":"Parent.TemplateWidth - 8","Height":"34","Size":"10",
   "Fill":f'If(varTipo = ThisItem.Value, Switch(ThisItem.Value, "New hire", ColorValue("#1E7B34"), "Termination", ColorValue("#B3261E"), ColorValue("#3E7CB1")), {LIGHT})',
   "Color":f'If(varTipo = ThisItem.Value, Color.White, {NAVY})',"HoverFill":'ColorValue("#C9C9D6")',"FontWeight":"FontWeight.Semibold","BorderThickness":"0",
   "OnSelect":'Set(varTipo, ThisItem.Value); Set(varEmp, {N: "", C: ""})',**pill(17)},indent=6)]))

# column captions
for i,(t,vis) in enumerate([('"WHO"',FORM),('If(varTipo = "Termination", "OFFBOARDING", "ROLE DETAILS")',FORM),('"SELECT FROM LISTS"',FORM)]):
    A(label(f"lblSec{i}R",t,cx(i),"118",CW,"22",9,GREY,True,vis))
def cap(name, text, i, y, vis): A(label(name,text,cx(i),str(y),CW,"20",9,NAVY,True,vis))
SEL={"BorderColor":'ColorValue("#C9C9D6")',"BorderThickness":"1","Align":"Align.Left","PaddingLeft":"12"}
def selbtn(name, text, i, y, onselect, vis, h="36"):
    A(button(name, text, cx(i), str(y), CW, h, onselect, fill="Color.White", color=NAVY, visible=vis, size=10, extra=SEL, r=8))
def picker(name, field, title, i, y, vis, key):
    cap("lblCap"+name, f'"{title}"', i, y, vis)
    selbtn("btn"+name, f'If(IsBlank({field}.N), "Select person  ▾", {field}.N & "  ·  " & {field}.C & "  ▾")', i, y+20, f'Set(varPick, "{key}")', vis)
def lista(name, var, title, items, i, y, key, vis):
    cap("lblCap"+name, f'"{title}" & If(!IsBlank({var}) && !({var} in {items}), "   (current: " & {var} & ", not standard)", "")', i, y, vis)
    selbtn("btn"+name, f'If(IsBlank({var}) || !({var} in {items}), "Select  ▾", {var} & "  ▾")', i, y+20, f'Set(varLista, "{key}")', vis)

ROLE=f"{FORM} && !({TERM})"; TV=f"{FORM} && {TERM}"
# column 0: WHO
cap("lblCapNombreR",'If(varTipo = "New hire", "Full name", "Employee")',0,146,FORM)
A(textinput("txtNombreR",'""',"First Last",cx(0),"166",CW,"36",f"{FORM} && {NEW}"))
selbtn("btnEmpR",'If(IsBlank(varEmp.N), "Select employee  ▾", varEmp.N & "  ·  " & varEmp.C)',0,166,'Set(varPick, "emp")',f"{FORM} && !({NEW})")
cap("lblCapFechaR",'Switch(varTipo, "New hire", "Start date (MM/DD/YYYY)", "Termination", "Last day (MM/DD/YYYY)", "Effective date (MM/DD/YYYY)")',0,210,FORM)
A(textinput("txtFechaR",'""',"MM/DD/YYYY",cx(0),"230",CW,"36",FORM))
cap("lblCapPuestoR",'"Job title"',0,274,ROLE)
A(textinput("txtPuestoR","varF.Puesto","e.g. Quality Inspector",cx(0),"294",CW,"36",ROLE))
A(label("lblCapNotasR",'"Notes for IT"',cx(0),'If(varTipo = "Termination", 274, 338)',CW,"20",9,NAVY,True,FORM))
A(textinput("txtNotasR",'""',"Anything else IT should know",cx(0),'If(varTipo = "Termination", 294, 358)',CW,"110",FORM,multi=True))

# column 1: ROLE DETAILS
cap("lblCapDescR",'"Job description"',1,146,ROLE)
A(textinput("txtDescR","varF.Desc","What this person does",cx(1),"166",CW,"110",ROLE,multi=True))
cap("lblCapScopeR",'"Scope"',1,282,ROLE)
A(textinput("txtScopeR","varF.Scope","Areas, plants, customers or products they cover",cx(1),"302",CW,"70",ROLE,multi=True))
cap("lblCapSkillsR",'"Skills"',1,378,ROLE)
A(textinput("txtSkillsR","varF.Skills","e.g. CNC, GD&T, SAP",cx(1),"398",CW,"36",ROLE))
cap("lblCapAccR",'"Other systems / permissions"',1,442,ROLE)
A(textinput("txtAccesosR",'""',"Shared folders, software, distribution lists",cx(1),"462",CW,"36",ROLE))
# column 1: OFFBOARDING
cap("lblCapAutoR",'"Automatic reply for their mailbox"',1,146,TV)
A(textinput("txtAutoR",'If(IsBlank(varEmp.N), "", varEmp.N & " is no longer with Sussek. Please contact " & Coalesce(varReasign.N, "[name]") & " at " & Coalesce(varReasign.C, "[email]") & ". Thank you.")',
  "Automatic reply text",cx(1),"166",CW,"150",TV,multi=True))

# column 2: LISTS
lista("DeptR","varDept","Department",DEPTS,2,146,"dept",ROLE)
lista("CompR","varComp","Company",COMPS,2,210,"comp",ROLE)
lista("LocR","varLoc","Location",LOCS,2,274,"loc",ROLE)
picker("MgrR","varMgr","Manager",2,338,ROLE,"mgr")
picker("BackupR","varBackup","Backup (covers when absent)",2,402,ROLE,"backup")
picker("ReasignR","varReasign","Reassign their team to",2,146,TV,"reasign")
picker("MbxR","varMbx","Give mailbox access to",2,210,TV,"mbx")
A(label("lblCapEqR",'If(varTipo = "Termination", "Equipment to collect", "Equipment and access needed")',cx(2),'If(varTipo = "Termination", 274, 466)',CW,"20",9,NAVY,True,FORM))
A(button("btnEqR",'If(IsEmpty(colEquip), "Select  ▾", Concat(colEquip, Value, ", ") & "  ▾")',cx(2),'If(varTipo = "Termination", 294, 486)',CW,"56",
  'Set(varLista, "equip")',fill="Color.White",color=NAVY,visible=FORM,size=10,extra={**SEL,"VerticalAlign":"VerticalAlign.Middle"},r=8))

# validation + submit
DATE='IfError(DateValue(txtFechaR.Text, "en-US"), Blank())'
val=f'''If(
  {NEW} && IsBlank(txtNombreR.Text), "Enter the full name.",
  !({NEW}) && IsBlank(varEmp.C), "Select the employee.",
  IsBlank({DATE}), "Enter the date as MM/DD/YYYY.",
  !({TERM}) && IsBlank(txtPuestoR.Text), "Enter the job title.",
  !({TERM}) && !(varDept in {DEPTS}), "Pick a department.",
  !({TERM}) && !(varComp in {COMPS}), "Pick a company.",
  !({TERM}) && !(varLoc in {LOCS}), "Pick a location.",
  !({TERM}) && IsBlank(varMgr.C), "Select the manager.",
  "")'''
A(label("lblValR",val,X0,"Parent.Height - 56",f"{W} - 240","40",10,'ColorValue("#B3261E")',True,FORM))

def row(k,v): return f'"<tr><td style=\'background:#EEEEF5;width:200px\'><b>{k}</b></td><td>" & {v} & "</td></tr>"'
def ba(k,old,new): return f'"<tr><td style=\'background:#EEEEF5\'><b>{k}</b></td><td>" & {old} & "</td><td" & If({old} <> {new}, " style=\'color:#B3261E;font-weight:bold\'", "") & ">" & {new} & "</td></tr>"'
submit=f'''Set(varEnviando, true);
With({{fecha: {DATE}, nombre: If({NEW}, Trim(txtNombreR.Text), varEmp.N), correo: If({NEW}, "", Lower(Trim(varEmp.C))), equipo: Concat(colEquip, Value, ", ")}},
  Patch(PeopleRequests, Defaults(PeopleRequests), {{
    Title: nombre, RequestType: varTipo, Status: "Sent to IT", EmployeeEmail: correo, EffectiveDate: fecha,
    JobTitle: If({TERM}, "", txtPuestoR.Text), Department: If({TERM}, "", varDept), Company: If({TERM}, "", varComp), Location: If({TERM}, "", varLoc),
    ManagerEmail: If({TERM}, "", varMgr.C), ManagerName: If({TERM}, "", varMgr.N),
    JobDescription: If({TERM}, "", txtDescR.Text), Scope: If({TERM}, "", txtScopeR.Text), Skills: If({TERM}, "", txtSkillsR.Text), BackupEmail: If({TERM}, "", varBackup.C),
    Equipment: equipo, SystemsAccess: If({TERM}, "", txtAccesosR.Text),
    PreviousValues: If({CHG}, "Job title: " & varF.Puesto & " | Department: " & varF.Depto & " | Company: " & varF.Empresa & " | Location: " & varF.Loc & " | Manager: " & varMgrAntes.N, ""),
    ReassignTo: If({TERM}, varReasign.C, ""), MailboxAccessTo: If({TERM}, varMbx.C, ""), AutoReply: If({TERM}, txtAutoR.Text, ""),
    Notes: txtNotasR.Text, RequestedBy: User().FullName}});
  Office365Outlook.SendEmailV2(
    lblITR.Text,
    "[" & varTipo & "] " & nombre & " · " & Text(fecha, "mmm d, yyyy", "en-US"),
    "<div style='font-family:Arial;font-size:13px;color:#202054'>" &
    "<h2 style='color:" & Switch(varTipo, "New hire", "#1E7B34", "Termination", "#B3261E", "#3E7CB1") & "'>" & varTipo & ": " & nombre & "</h2>" &
    "<p>Requested by " & User().FullName & " (HR) on " & Text(Now(), "mmm d, yyyy", "en-US") & ".</p>" &
    "<table border='1' cellpadding='6' style='border-collapse:collapse;font-size:13px'>" &
    {row("Employee","nombre")} & {row("Email",'If(' + NEW + ', "To be assigned by IT", correo)')} &
    {row('" & Switch(varTipo, "New hire", "Start date", "Termination", "Last day", "Effective date") & "',"Text(fecha, \"dddd, mmm d, yyyy\", \"en-US\")")} &
    If({TERM},
      {row("Reassign their team to",'varReasign.N & " (" & varReasign.C & ")"')} &
      {row("Mailbox access to",'varMbx.N & " (" & varMbx.C & ")"')} &
      {row("Automatic reply","txtAutoR.Text")} &
      {row("Equipment to collect","equipo")},
      {row("Job title","txtPuestoR.Text")} & {row("Department","varDept")} & {row("Company","varComp")} & {row("Office location","varLoc")} &
      {row("Manager",'varMgr.N & " (" & varMgr.C & ")"')} & {row("Backup","varBackup.N")} &
      {row("Equipment and access","equipo")} & {row("Other systems","txtAccesosR.Text")}) &
    {row("Notes","txtNotasR.Text")} &
    "</table>" &
    If({CHG}, "<h3>Before and after</h3><table border='1' cellpadding='6' style='border-collapse:collapse;font-size:13px'><tr><th></th><th align='left'>Before</th><th align='left'>After</th></tr>" &
      {ba("Job title","varF.Puesto","txtPuestoR.Text")} & {ba("Department","varF.Depto","varDept")} & {ba("Company","varF.Empresa","varComp")} & {ba("Office location","varF.Loc","varLoc")} & {ba("Manager","varMgrAntes.N","varMgr.N")} & "</table>", "") &
    "<h3>Steps for IT</h3><ol>" &
    Switch(varTipo,
      "New hire",
        "<li>Create the account for <b>" & nombre & "</b> (you choose the email address) and assign a Microsoft 365 license. <b>Please reply with the new email address.</b></li>" &
        "<li>In Entra ID set exactly: Job title = <b>" & txtPuestoR.Text & "</b>, Department = <b>" & varDept & "</b>, Company name = <b>" & varComp & "</b>, Office location = <b>" & varLoc & "</b>, Manager = <b>" & varMgr.N & "</b>.</li>" &
        "<li>Prepare equipment and access: " & Coalesce(equipo, "none listed") & If(IsBlank(txtAccesosR.Text), "", "; " & txtAccesosR.Text) & ".</li>" &
        "<li>Everything ready before <b>" & Text(fecha, "mmm d, yyyy", "en-US") & "</b>.</li>",
      "Termination",
        "<li>On <b>" & Text(fecha, "mmm d, yyyy", "en-US") & "</b> at end of day, <b>block sign-in</b> (do not delete the account).</li>" &
        "<li>Convert the mailbox to a <b>shared mailbox</b> and give access to <b>" & varMbx.N & "</b>.</li>" &
        "<li>Set the automatic reply above.</li>" &
        "<li><b>Hide from address lists</b> (GAL).</li>" &
        "<li>In Entra ID, change the Manager of their direct reports to <b>" & varReasign.N & "</b>.</li>" &
        "<li>Remove licenses.</li>" &
        "<li>Collect equipment: " & Coalesce(equipo, "none listed") & ".</li>",
      "<li>On <b>" & Text(fecha, "mmm d, yyyy", "en-US") & "</b>, update Entra ID with the values in the After column (highlighted in red).</li>" &
      If(IsBlank(equipo) && IsBlank(txtAccesosR.Text), "", "<li>Equipment and access: " & equipo & " " & txtAccesosR.Text & "</li>")) &
    "</ol><p>Please reply to this email when it's done.</p></div>",
    {{Cc: User().Email, Importance: "Normal"}});
  If({CHG},
    IfError(
      If(IsBlank(LookUp(Organigrama, Lower(Correo) = correo)),
        Patch(Organigrama, Defaults(Organigrama), {{Title: nombre, Correo: correo, Puesto: txtPuestoR.Text, Area: varDept, CorreoJefe: varMgr.C, Descripcion: txtDescR.Text, Scope: txtScopeR.Text, Skills: txtSkillsR.Text, Backup: varBackup.C, Location: varLoc}}),
        Patch(Organigrama, LookUp(Organigrama, Lower(Correo) = correo), {{Title: nombre, Correo: correo, Puesto: txtPuestoR.Text, Area: varDept, CorreoJefe: varMgr.C, Descripcion: txtDescR.Text, Scope: txtScopeR.Text, Skills: txtSkillsR.Text, Backup: varBackup.C, Location: varLoc}}));
      true,
      Notify("Sent to IT, but the org chart list could not be updated.", NotificationType.Warning)))
);
Notify("Request sent to IT", NotificationType.Success);
Set(varEnviando, false);
Set(varModo, "");
Set(varFiltroT, "All")'''
A(button("btnSendR",'If(varEnviando, "Sending...", "Send to IT")',"Parent.Width - 220","Parent.Height - 60","200","44",submit,visible=FORM,size=12,
  extra={"DisplayMode":"If(IsBlank(lblValR.Text) && !varEnviando, DisplayMode.Edit, DisplayMode.Disabled)"}))

# ---------- detail view ----------
VIEW='varModo = "view"'
det=('varSel.RequestType & ":  " & varSel.Title & Char(10) & Char(10) & '
 '"Status:             " & varSel.Status & Char(10) & '
 '"Email:              " & varSel.EmployeeEmail & Char(10) & '
 'Switch(varSel.RequestType, "New hire", "Start date:         ", "Termination", "Last day:           ", "Effective date:     ") & Text(varSel.EffectiveDate, "dddd, mmm d, yyyy", "en-US") & Char(10) & '
 '"Requested by:       " & varSel.RequestedBy & " on " & Text(varSel.Created, "mmm d, yyyy", "en-US") & Char(10) & Char(10) & '
 'If(varSel.RequestType = "Termination", '
 '"Reassign team to:   " & varSel.ReassignTo & Char(10) & "Mailbox access to:  " & varSel.MailboxAccessTo & Char(10) & "Automatic reply:    " & varSel.AutoReply & Char(10) & "Equipment:          " & varSel.Equipment, '
 '"Job title:          " & varSel.JobTitle & Char(10) & "Department:         " & varSel.Department & Char(10) & "Company:            " & varSel.Company & Char(10) & "Location:           " & varSel.Location & Char(10) & '
 '"Manager:            " & varSel.ManagerName & "  (" & varSel.ManagerEmail & ")" & Char(10) & "Backup:             " & varSel.BackupEmail & Char(10) & '
 '"Equipment:          " & varSel.Equipment & Char(10) & "Other systems:      " & varSel.SystemsAccess & Char(10) & Char(10) & '
 '"Job description:" & Char(10) & varSel.JobDescription & Char(10) & Char(10) & "Scope:" & Char(10) & varSel.Scope & Char(10) & Char(10) & "Skills:  " & varSel.Skills & '
 'If(IsBlank(varSel.PreviousValues), "", Char(10) & Char(10) & "Before the change:" & Char(10) & varSel.PreviousValues)) & '
 'Char(10) & Char(10) & "Notes:  " & varSel.Notes')
A(label("lblDetR",det,X0,"76",f"{W}","Parent.Height - 170",11,NAVY,False,VIEW,
  {"VerticalAlign":"VerticalAlign.Top","Fill":"Color.White","BorderColor":'ColorValue("#E3E3E3")',"BorderThickness":"1","PaddingTop":"18","PaddingLeft":"22","PaddingRight":"22","PaddingBottom":"18"}))
A(label("lblAsigCapR",'"Email assigned by IT"',"Parent.Width - 520","Parent.Height - 82","280","20",9,NAVY,True,'varModo = "view" && varSel.RequestType = "New hire" && varSel.Status <> "Done"'))
A(textinput("txtAsigR",'""',"name@sussek.com","Parent.Width - 520","Parent.Height - 60","280","44",'varModo = "view" && varSel.RequestType = "New hire" && varSel.Status <> "Done"'))
done_fx='''If(varSel.Status = "Done",
  Patch(PeopleRequests, varSel, {Status: "Sent to IT"}),
  If(varSel.RequestType = "New hire",
    With({c: Lower(Trim(txtAsigR.Text))},
      Patch(PeopleRequests, varSel, {Status: "Done", EmployeeEmail: c});
      IfError(
        If(IsBlank(LookUp(Organigrama, Lower(Correo) = c)),
          Patch(Organigrama, Defaults(Organigrama), {Title: varSel.Title, Correo: c, Puesto: varSel.JobTitle, Area: varSel.Department, CorreoJefe: varSel.ManagerEmail, Descripcion: varSel.JobDescription, Scope: varSel.Scope, Skills: varSel.Skills, Backup: varSel.BackupEmail, Location: varSel.Location, StartDate: varSel.EffectiveDate}),
          Patch(Organigrama, LookUp(Organigrama, Lower(Correo) = c), {Title: varSel.Title, Correo: c, Puesto: varSel.JobTitle, Area: varSel.Department, CorreoJefe: varSel.ManagerEmail, Descripcion: varSel.JobDescription, Scope: varSel.Scope, Skills: varSel.Skills, Backup: varSel.BackupEmail, Location: varSel.Location, StartDate: varSel.EffectiveDate}));
        true,
        Notify("Marked as done, but the org chart list could not be updated.", NotificationType.Warning))),
    Patch(PeopleRequests, varSel, {Status: "Done"})));
Reset(txtAsigR);
Set(varSel, LookUp(PeopleRequests, ID = varSel.ID))'''
A(button("btnDoneR",'If(varSel.Status = "Done", "Reopen", "✓ Mark as done")',"Parent.Width - 220","Parent.Height - 60","200","44",done_fx,visible=VIEW,size=12,
  extra={"DisplayMode":'If(varSel.RequestType = "New hire" && varSel.Status <> "Done" && !IsMatch(txtAsigR.Text, Match.Email), DisplayMode.Disabled, DisplayMode.Edit)'}))

# ---------- person picker overlay ----------
PV='!IsBlank(varPick)'
A(ctrl("recDimR","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.Width","Height":"Parent.Height","Fill":"RGBA(32, 32, 84, 0.45)","Visible":PV,"OnSelect":'Set(varPick, "")'}))
A(ctrl("recPickR","Rectangle@2.3.0",{"X":"(Parent.Width - 520) / 2","Y":"90","Width":"520","Height":"480","Fill":"Color.White","Visible":PV}))
A(label("lblPickR",'Switch(varPick, "emp", "Select the employee", "mgr", "Select the manager", "backup", "Select the backup", "reasign", "Who takes over their team?", "Who gets access to their mailbox?")',
  "(Parent.Width - 520) / 2 + 24","104","400","36",13,NAVY,True,PV))
A(button("btnPickCloseR",'"✕"',"(Parent.Width - 520) / 2 + 470","104","36","36",'Set(varPick, "")',fill="Color.Transparent",color=NAVY,visible=PV,size=13))
A(textinput("txtPickR",'""',"Type at least 2 letters of the name","(Parent.Width - 520) / 2 + 24","146","472","40",PV))
pickset='''With({rec: {N: ThisItem.DisplayName, C: Lower(Coalesce(ThisItem.Mail, ThisItem.UserPrincipalName))}},
  Switch(varPick,
    "emp",
      With({m: IfError(UsuariosdeOffice365.ManagerV2(ThisItem.Id, {'$select': "displayName,mail"}), Blank()), o: LookUp(Organigrama, Lower(Correo) = rec.C)},
        Set(varEmp, rec);
        Set(varMgr, {N: Coalesce(m.displayName, ""), C: Lower(Coalesce(m.mail, ""))});
        Set(varMgrAntes, varMgr);
        Set(varBackup, {N: Coalesce(o.Backup, ""), C: Coalesce(o.Backup, "")});
        Set(varF, {Puesto: Coalesce(ThisItem.JobTitle, ""), Depto: Coalesce(ThisItem.Department, ""), Empresa: Coalesce(ThisItem.CompanyName, ""), Loc: Coalesce(o.Location, ThisItem.OfficeLocation, ""), Desc: Coalesce(o.Descripcion, ""), Scope: Coalesce(o.Scope, ""), Skills: Coalesce(o.Skills, "")});
        Set(varDept, varF.Depto); Set(varComp, varF.Empresa); Set(varLoc, varF.Loc)),
    "mgr", Set(varMgr, rec),
    "backup", Set(varBackup, rec),
    "reasign", Set(varReasign, rec),
    Set(varMbx, rec)));
Set(varPick, ""); Reset(txtPickR)'''
A(ctrl("galPickR","Gallery@2.15.0",{"Items":'If(Len(txtPickR.Text) >= 2, Filter(UsuariosdeOffice365.SearchUserV2({searchTerm: txtPickR.Text, top: 15}).value, AccountEnabled))',
  "X":"(Parent.Width - 520) / 2 + 24","Y":"196","Width":"472","Height":"360","TemplateSize":"56","TemplatePadding":"0","ShowScrollbar":"true","Visible":PV},variant="Vertical",children=[
  ctrl("btnPickRowR","Classic/Button@2.2.0",{"Text":'""',"X":"0","Y":"0","Width":"Parent.TemplateWidth","Height":"Parent.TemplateHeight - 2","Fill":"Color.White","HoverFill":LIGHT,"PressedFill":'ColorValue("#E2E2EE")',
    "BorderThickness":"0","OnSelect":pickset,**pill(0)},indent=6),
  ctrl("lblPickNameR","Label@2.5.1",{"Text":"ThisItem.DisplayName","X":"12","Y":"4","Width":"Parent.TemplateWidth - 24","Height":"26","Size":"11","FontWeight":"FontWeight.Bold","Color":NAVY},indent=6),
  ctrl("lblPickInfoR","Label@2.5.1",{"Text":'Coalesce(ThisItem.JobTitle, "-") & "  ·  " & Coalesce(ThisItem.Department, "-") & "  ·  " & Coalesce(ThisItem.Mail, ThisItem.UserPrincipalName)',
    "X":"12","Y":"28","Width":"Parent.TemplateWidth - 24","Height":"22","Size":"9","Color":GREY},indent=6)]))


# ---------- list picker overlay ----------
LV='!IsBlank(varLista)'
A(ctrl("recDimLR","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.Width","Height":"Parent.Height","Fill":"RGBA(32, 32, 84, 0.45)","Visible":LV,"OnSelect":'Set(varLista, "")'}))
A(ctrl("recListaR","Rectangle@2.3.0",{"X":"(Parent.Width - 420) / 2","Y":"80","Width":"420","Height":"Parent.Height - 160","Fill":"Color.White","Visible":LV}))
A(label("lblListaR",'Switch(varLista, "dept", "Department", "comp", "Company", "loc", "Location", If(varTipo = "Termination", "Equipment to collect (pick all)", "Equipment and access (pick all)"))',
  "(Parent.Width - 420) / 2 + 24","94","300","36",13,NAVY,True,LV))
A(button("btnListaOkR",'If(varLista = "equip", "Done", "✕")',"(Parent.Width - 420) / 2 + 420 - 96","94","80","36",'Set(varLista, "")',visible=LV,size=11))
A(ctrl("galListaR","Gallery@2.15.0",{"Items":f'Switch(varLista, "dept", {DEPTS}, "comp", {COMPS}, "loc", {LOCS}, {EQUIP})',
  "X":"(Parent.Width - 420) / 2 + 16","Y":"140","Width":"388","Height":"Parent.Height - 236","TemplateSize":"46","TemplatePadding":"0","ShowScrollbar":"true","Visible":LV},variant="Vertical",children=[
  ctrl("btnListaRowR","Classic/Button@2.2.0",{"Text":'If(Switch(varLista, "dept", varDept, "comp", varComp, "loc", varLoc, "") = ThisItem.Value || (varLista = "equip" && ThisItem.Value in colEquip.Value), "✓   ", "     ") & ThisItem.Value',
    "X":"0","Y":"0","Width":"Parent.TemplateWidth","Height":"Parent.TemplateHeight - 2","Size":"11","Align":"Align.Left","PaddingLeft":"16",
    "Fill":'If(Switch(varLista, "dept", varDept, "comp", varComp, "loc", varLoc, "") = ThisItem.Value || (varLista = "equip" && ThisItem.Value in colEquip.Value), ColorValue("#EEEEF5"), Color.White)',
    "HoverFill":'ColorValue("#E2E2EE")',"Color":NAVY,"BorderThickness":"0",
    "OnSelect":'''Switch(varLista,
  "dept", Set(varDept, ThisItem.Value); Set(varLista, ""),
  "comp", Set(varComp, ThisItem.Value); Set(varLista, ""),
  "loc", Set(varLoc, ThisItem.Value); Set(varLista, ""),
  If(ThisItem.Value in colEquip.Value, Remove(colEquip, LookUp(colEquip, Value = ThisItem.Value)), Collect(colEquip, {Value: ThisItem.Value})))''',**pill(0)},indent=6)]))

open('/home/user/claude/altas-bajas/Pantalla-PeopleRequests-COPIAR.txt','w').write("\n".join(out)+"\n")
open('/home/user/claude/altas-bajas/btnSendR-COPIAR.txt','w').write([x for x in out if x.startswith('- btnSendR:')][0]+"\n")
