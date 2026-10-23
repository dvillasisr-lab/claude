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
Reset(txtNombreR); Reset(txtCorreoR); Reset(txtFechaR); Reset(txtPuestoR); Reset(txtDescR); Reset(txtScopeR); Reset(txtSkillsR); Reset(txtAccesosR); Reset(txtNotasR); Reset(txtAutoR)''',
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
for i,(t,vis) in enumerate([('"WHO"',FORM),('If(varTipo = "Termination", "OFFBOARDING", "ROLE")',FORM),('"DETAILS"',f'{FORM} && !({TERM})')]):
    A(label(f"lblSec{i}R",t,cx(i),"118",CW,"22",9,GREY,True,vis))
def cap(name, text, i, y, vis): A(label(name,text,cx(i),str(y),CW,"20",9,NAVY,True,vis))
def picker(name, field, title, i, y, vis, key):
    cap("lblCap"+name, f'"{title}"', i, y, vis)
    A(button("btn"+name, f'If(IsBlank({field}.N), "Select person  ▾", {field}.N & "  ·  " & {field}.C)', cx(i), str(y+20), CW, "36",
      f'Set(varPick, "{key}")', fill="Color.White", color=NAVY, visible=vis, size=10,
      extra={"BorderColor":'ColorValue("#C9C9D6")',"BorderThickness":"1","Align":"Align.Left","PaddingLeft":"12"}, r=8))

# column 0
cap("lblCapNombreR",'If(varTipo = "New hire", "Full name", "Employee")',0,146,FORM)
A(textinput("txtNombreR",'""',"First Last",cx(0),"166",CW,"36",f"{FORM} && {NEW}"))
A(button("btnEmpR",'If(IsBlank(varEmp.N), "Select employee  ▾", varEmp.N)',cx(0),"166",CW,"36",'Set(varPick, "emp")',fill="Color.White",color=NAVY,
  visible=f"{FORM} && !({NEW})",size=10,extra={"BorderColor":'ColorValue("#C9C9D6")',"BorderThickness":"1","Align":"Align.Left","PaddingLeft":"12"},r=8))
cap("lblCapCorreoR",'If(varTipo = "New hire", "Email to create", "Email")',0,210,FORM)
A(textinput("txtCorreoR",'""',"jdoe@sussek.com",cx(0),"230",CW,"36",f"{FORM} && {NEW}"))
A(label("lblCorreoR",'Coalesce(varEmp.C, "-")',cx(0),"230",CW,"36",11,GREY,False,f"{FORM} && !({NEW})"))
cap("lblCapFechaR",'Switch(varTipo, "New hire", "Start date (MM/DD/YYYY)", "Termination", "Last day (MM/DD/YYYY)", "Effective date (MM/DD/YYYY)")',0,274,FORM)
A(textinput("txtFechaR",'""',"MM/DD/YYYY",cx(0),"294",CW,"36",FORM))
picker("MgrR","varMgr","Manager",0,338,f"{FORM} && !({TERM})","mgr")
picker("BackupR","varBackup","Backup (covers when absent)",0,402,f"{FORM} && !({TERM})","backup")
picker("ReasignR","varReasign","Reassign their team to",0,338,f"{FORM} && {TERM}","reasign")
picker("MbxR","varMbx","Give mailbox access to",0,402,f"{FORM} && {TERM}","mbx")
cap("lblCapNotasR",'"Notes for IT"',0,466,FORM)
A(textinput("txtNotasR",'""',"Anything else IT should know",cx(0),"486",CW,"90",FORM,multi=True))

# column 1 (role)
ROLE=f"{FORM} && !({TERM})"
cap("lblCapPuestoR",'"Job title"',1,146,ROLE)
A(textinput("txtPuestoR","varF.Puesto","e.g. Quality Inspector",cx(1),"166",CW,"36",ROLE))
cap("lblCapDeptR",'"Department" & If(!IsBlank(varDept) && !(varDept in ' + DEPTS + '), "   (current: " & varDept & ", pick a standard one)", "")',1,210,ROLE)
A(chips("DeptR",DEPTS,cx(1),"232",CW,"196","varDept = ThisItem.Value","Set(varDept, ThisItem.Value)",ROLE,2,28))
cap("lblCapCompR",'"Company" & If(!IsBlank(varComp) && !(varComp in ' + COMPS + '), "   (current: " & varComp & ")", "")',1,432,ROLE)
A(chips("CompR",COMPS,cx(1),"452",CW,"84","varComp = ThisItem.Value","Set(varComp, ThisItem.Value)",ROLE,2,28))
cap("lblCapLocR",'"Location" & If(!IsBlank(varLoc) && !(varLoc in ' + LOCS + '), "   (current: " & varLoc & ")", "")',1,540,ROLE)
A(chips("LocR",LOCS,cx(1),"560",CW,"56","varLoc = ThisItem.Value","Set(varLoc, ThisItem.Value)",ROLE,2,28))
# column 1 (termination)
TV=f"{FORM} && {TERM}"
cap("lblCapAutoR",'"Automatic reply for their mailbox"',1,146,TV)
A(textinput("txtAutoR",'If(IsBlank(varEmp.N), "", varEmp.N & " is no longer with Sussek. Please contact " & Coalesce(varReasign.N, "[name]") & " at " & Coalesce(varReasign.C, "[email]") & ". Thank you.")',
  "Automatic reply text",cx(1),"166",CW,"130",TV,multi=True))
cap("lblCapEqOutR",'"Equipment to collect"',1,304,TV)
A(chips("EqOutR",EQUIP,cx(1),"324",CW,"150","ThisItem.Value in colEquip.Value",
  "If(ThisItem.Value in colEquip.Value, Remove(colEquip, LookUp(colEquip, Value = ThisItem.Value)), Collect(colEquip, {Value: ThisItem.Value}))",TV,2,28))

# column 2 (details)
cap("lblCapDescR",'"Job description"',2,146,ROLE)
A(textinput("txtDescR","varF.Desc","What this person does",cx(2),"166",CW,"110",ROLE,multi=True))
cap("lblCapScopeR",'"Scope"',2,282,ROLE)
A(textinput("txtScopeR","varF.Scope","Areas, plants, customers or products they cover",cx(2),"302",CW,"70",ROLE,multi=True))
cap("lblCapSkillsR",'"Skills"',2,378,ROLE)
A(textinput("txtSkillsR","varF.Skills","e.g. CNC, GD&T, SAP",cx(2),"398",CW,"36",ROLE))
cap("lblCapEqR",'"Equipment and access needed"',2,440,ROLE)
A(chips("EqR",EQUIP,cx(2),"460",CW,"116","ThisItem.Value in colEquip.Value",
  "If(ThisItem.Value in colEquip.Value, Remove(colEquip, LookUp(colEquip, Value = ThisItem.Value)), Collect(colEquip, {Value: ThisItem.Value}))",ROLE,2,23))
cap("lblCapAccR",'"Other systems / permissions"',2,580,ROLE)
A(textinput("txtAccesosR",'""',"Shared folders, software, distribution lists",cx(2),"600",CW,"36",ROLE))

# validation + submit
DATE='IfError(DateValue(txtFechaR.Text, "en-US"), Blank())'
val=f'''If(
  {NEW} && IsBlank(txtNombreR.Text), "Enter the full name.",
  !({NEW}) && IsBlank(varEmp.C), "Select the employee.",
  {NEW} && !IsMatch(txtCorreoR.Text, Match.Email), "Enter the email IT should create.",
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
With({{fecha: {DATE}, nombre: If({NEW}, Trim(txtNombreR.Text), varEmp.N), correo: Lower(Trim(If({NEW}, txtCorreoR.Text, varEmp.C))), equipo: Concat(colEquip, Value, ", ")}},
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
    {row("Employee","nombre")} & {row("Email","correo")} &
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
        "<li>Create the account <b>" & correo & "</b> and assign a Microsoft 365 license.</li>" &
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
  If(!({TERM}),
    IfError(
      With({{o: LookUp(Organigrama, Lower(Correo) = correo)}},
        With({{r: Patch(Organigrama, If(IsBlank(o), Defaults(Organigrama), o), {{Title: nombre, Correo: correo, Puesto: txtPuestoR.Text, Area: varDept, CorreoJefe: varMgr.C, Descripcion: txtDescR.Text, Scope: txtScopeR.Text, Skills: txtSkillsR.Text, Backup: varBackup.C, Location: varLoc}})}},
          If({NEW}, Patch(Organigrama, r, {{StartDate: fecha}})))),
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
A(label("lblDetR",det,X0,"76",f"{W}","Parent.Height - 150",11,NAVY,False,VIEW,
  {"VerticalAlign":"VerticalAlign.Top","Fill":"Color.White","BorderColor":'ColorValue("#E3E3E3")',"BorderThickness":"1","PaddingTop":"18","PaddingLeft":"22","PaddingRight":"22","PaddingBottom":"18"}))
A(button("btnDoneR",'If(varSel.Status = "Done", "Reopen", "✓ Mark as done")',"Parent.Width - 220","Parent.Height - 60","200","44",
  'Patch(PeopleRequests, varSel, {Status: If(varSel.Status = "Done", "Sent to IT", "Done")}); Set(varSel, LookUp(PeopleRequests, ID = varSel.ID))',visible=VIEW,size=12))

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

open('/home/user/claude/altas-bajas/Pantalla-PeopleRequests-COPIAR.txt','w').write("\n".join(out)+"\n")
