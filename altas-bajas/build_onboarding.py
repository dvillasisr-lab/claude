exec(open('helpers.py').read())
ONB=[("Offer letter signed","HR","1. Before day 1",-7,"Document","Personnel file"),
("Background check / drug screen results","HR","1. Before day 1",-3,"Document","Confidential file"),
("People Request sent to IT","HR","1. Before day 1",-7,"Task",""),
("Workstation, tools and PPE ready","Manager","1. Before day 1",-1,"Task",""),
("First-week schedule and trainer assigned","Manager","1. Before day 1",-1,"Task",""),
("Account, computer and phone ready","IT","1. Before day 1",-1,"Task",""),
("I-9 Section 1 (employee)","HR","2. Day 1",0,"Document","I-9 binder (separate)"),
("W-4 federal withholding","HR","2. Day 1",0,"Document","Payroll file"),
("State withholding form","HR","2. Day 1",0,"Document","Payroll file"),
("Direct deposit form","HR","2. Day 1",0,"Document","Payroll file"),
("Emergency contact form","HR","2. Day 1",0,"Document","Personnel file"),
("Employee handbook acknowledgment","HR","2. Day 1",0,"Document","Personnel file"),
("Confidentiality / NDA","HR","2. Day 1",0,"Document","Personnel file"),
("Drug and alcohol policy acknowledgment","HR","2. Day 1",0,"Document","Personnel file"),
("Badge / keys issued","HR","2. Day 1",0,"Task",""),
("Safety orientation","EHS","2. Day 1",0,"Document","Training file"),
("PPE issued (glasses, shoes, gloves, hearing)","EHS","2. Day 1",0,"Document","Training file"),
("Welcome and team introduction","Manager","2. Day 1",0,"Task",""),
("I-9 Section 2 verified (within 3 business days)","HR","3. First 2 weeks",3,"Document","I-9 binder (separate)"),
("Hazard communication (HazCom) training","EHS","3. First 2 weeks",5,"Document","Training file"),
("Job-specific training plan started","Manager","3. First 2 weeks",5,"Task",""),
("Forklift / equipment certification (if applicable)","EHS","3. First 2 weeks",14,"Document","Training file"),
("Benefits enrollment form","HR","4. 30 days",30,"Document","Benefits file (confidential)"),
("30-day check-in","Manager","4. 30 days",30,"Task",""),
("90-day performance review","Manager","5. 90 days",90,"Document","Personnel file"),
("End of probation confirmed","HR","5. 90 days",90,"Task","")]
OFF=[("People Request sent to IT","HR","1. Before last day",-5,"Task",""),
("Exit interview scheduled","HR","1. Before last day",-5,"Task",""),
("Knowledge transfer to backup","Manager","1. Before last day",-3,"Task",""),
("Final paycheck and PTO payout calculated","HR","1. Before last day",-2,"Document","Payroll file"),
("Equipment returned (laptop, phone, tools, PPE)","Manager","2. Last day",0,"Task",""),
("Badge / keys returned","HR","2. Last day",0,"Task",""),
("Exit interview completed","HR","2. Last day",0,"Document","Personnel file"),
("Sign-in blocked and mailbox shared","IT","2. Last day",0,"Task",""),
("Final paycheck delivered","HR","3. After",7,"Task",""),
("COBRA / benefits termination notice sent","HR","3. After",14,"Document","Benefits file (confidential)"),
("Personnel file closed","HR","3. After",30,"Task","")]
def tbl(rows): return "Table(\n    " + ",\n    ".join('{Task: "%s", Owner: "%s", Phase: "%s", Days: %d, Kind: "%s", Filed: "%s"}' % r for r in rows) + ")"

OWNC='Switch(ThisItem.Owner, "HR", ColorValue("#6A5A8C"), "Manager", ColorValue("#2E5C8A"), "EHS", ColorValue("#B36B00"), ColorValue("#3E7CB1"))'
X0="400"; W="(Parent.Width - 420)"
HIRE='!IsBlank(varHire)'
LOADED=f'{HIRE} && !IsEmpty(colTasks)'

A(ctrl("recHeadO","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.Width","Height":"64","Fill":NAVY}))
A(button("btnBackO",'"←"',"8","12","40","40","Back()",fill="Color.Transparent",size=16))
A(label("lblTitleO",'"Onboarding & Offboarding"',"56","0","360","64",16,"Color.White",True))
A(label("lblEHSCapO",'"EHS email:"',"Parent.Width - 400","0","90","64",10,'ColorValue("#C9C9D6")'))
A(label("lblEHSO",'"CORREO_DE_EHS@sussek.com"',"Parent.Width - 310","0","290","64",11,"Color.White",True))

# left list
A(ctrl("recLeftO","Rectangle@2.3.0",{"X":"0","Y":"64","Width":"380","Height":"Parent.Height - 64","Fill":'ColorValue("#F6F6FA")'}))
A(ctrl("galTabsO","Gallery@2.15.0",{"Items":'["New hire", "Termination"]',"X":"12","Y":"76","Width":"356","Height":"34","WrapCount":"2","TemplateSize":"34","TemplatePadding":"0","ShowScrollbar":"false"},variant="Vertical",children=[
  ctrl("btnTabO","Classic/Button@2.2.0",{"Text":'If(ThisItem.Value = "New hire", "New hires", "Terminations")',"X":"0","Y":"0","Width":"Parent.TemplateWidth - 6","Height":"30","Size":"10",
   "Fill":f'If(Coalesce(varTabO, "New hire") = ThisItem.Value, {NAVY}, Color.White)',"Color":f'If(Coalesce(varTabO, "New hire") = ThisItem.Value, Color.White, {NAVY})',
   "HoverFill":'ColorValue("#C9C9D6")',"BorderThickness":"0","OnSelect":"Set(varTabO, ThisItem.Value)",**pill(15)},indent=6)]))
sel='Set(varHire, ThisItem); Set(varOwnerO, "All"); ClearCollect(colTasks, Filter(OnboardingTasks, RequestID = ThisItem.ID))'
A(ctrl("galHiresO","Gallery@2.15.0",{"Items":'Sort(Filter(PeopleRequests, RequestType = Coalesce(varTabO, "New hire")), EffectiveDate, SortOrder.Descending)',
  "X":"12","Y":"118","Width":"356","Height":"Parent.Height - 128","TemplateSize":"78","TemplatePadding":"0","ShowScrollbar":"true"},variant="Vertical",children=[
  ctrl("recRowO","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.TemplateWidth","Height":"Parent.TemplateHeight - 6",
    "Fill":'If(!IsBlank(varHire) && varHire.ID = ThisItem.ID, ColorValue("#E2E2EE"), Color.White)',"BorderColor":'ColorValue("#E3E3E3")',"BorderThickness":"1","OnSelect":sel},indent=6),
  ctrl("lblHireNameO","Label@2.5.1",{"OnSelect":"Select(recRowO)","Text":"ThisItem.Title","X":"12","Y":"6","Width":"Parent.TemplateWidth - 24","Height":"26","Size":"11","FontWeight":"FontWeight.Bold","Color":NAVY},indent=6),
  ctrl("lblHireInfoO","Label@2.5.1",{"OnSelect":"Select(recRowO)",
    "Text":'If(ThisItem.RequestType = "Termination", "Last day ", "Start ") & Text(ThisItem.EffectiveDate, "mmm d, yyyy", "en-US") & "  ·  " & With({t: CountRows(Filter(OnboardingTasks, RequestID = ThisItem.ID)), d: CountRows(Filter(OnboardingTasks, RequestID = ThisItem.ID && Status = "Done"))}, If(t = 0, "Checklist not started", d & " of " & t & " done"))',
    "X":"12","Y":"34","Width":"Parent.TemplateWidth - 24","Height":"30","Size":"9","Color":GREY},indent=6)]))

A(label("lblEmptyO",'"Select a person on the left."',X0,"300",W,"40",12,GREY,False,"IsBlank(varHire)",{"Align":"Align.Center"}))

# selected header
A(label("lblHireO",'varHire.Title',X0,"76","(Parent.Width - 420) - 420","36",16,NAVY,True,HIRE))
A(label("lblHireSubO",'varHire.RequestType & "  ·  " & If(varHire.RequestType = "Termination", "Last day ", "Start date ") & Text(varHire.EffectiveDate, "dddd, mmm d, yyyy", "en-US") & If(IsBlank(varHire.JobTitle), "", "  ·  " & varHire.JobTitle & "  ·  " & varHire.Department)',
  X0,"110",f"{W} - 420","24",10,GREY,False,HIRE))
start=f'''With({{tpl: If(varHire.RequestType = "Termination",
  {tbl(OFF)},
  {tbl(ONB)})}},
  ForAll(tpl As t,
    Patch(OnboardingTasks, Defaults(OnboardingTasks), {{Title: t.Task, RequestID: varHire.ID, Employee: varHire.Title, Owner: t.Owner, Phase: t.Phase, DueDate: DateAdd(varHire.EffectiveDate, t.Days, TimeUnit.Days), Status: "Pending", DoneBy: "", FiledIn: t.Filed, Kind: t.Kind, Notes: ""}})));
ClearCollect(colTasks, Filter(OnboardingTasks, RequestID = varHire.ID));
Notify("Checklist created", NotificationType.Success)'''
A(button("btnStartO",'"Start " & If(varHire.RequestType = "Termination", "offboarding", "onboarding") & " checklist"',f"{X0} + ({W} - 320) / 2","260","320","52",start,
  visible=f"{HIRE} && IsEmpty(colTasks)",size=13))
A(label("lblStartInfoO",'"Creates the task list for HR, the manager, EHS and IT, with due dates based on the " & If(varHire.RequestType = "Termination", "last day.", "start date.")',
  X0,"320",W,"30",10,GREY,False,f"{HIRE} && IsEmpty(colTasks)",{"Align":"Align.Center"}))

# progress bar
DONE='CountRows(Filter(colTasks, Status = "Done"))'
A(ctrl("recBarBgO","Rectangle@2.3.0",{"X":X0,"Y":"142","Width":f"{W} - 420","Height":"10","Fill":'ColorValue("#E2E2EE")',"Visible":LOADED}))
A(ctrl("recBarO","Rectangle@2.3.0",{"X":X0,"Y":"142","Width":f'({W} - 420) * {DONE} / Max(1, CountRows(colTasks))',"Height":"10","Fill":'ColorValue("#1E7B34")',"Visible":LOADED}))
A(label("lblBarO",f'{DONE} & " of " & CountRows(colTasks) & " done" & With({{o: CountRows(Filter(colTasks, Status <> "Done" && DueDate < Today()))}}, If(o > 0, "   ·   " & o & " overdue", ""))',
  f"{X0} + {W} - 410","132","400","30",10,NAVY,True,LOADED))

mail=f'''ForAll(Table({{O: "Manager", To: Coalesce(varHire.ManagerEmail, varHire.ReassignTo)}}, {{O: "EHS", To: lblEHSO.Text}}, {{O: "IT", To: lblITR.Text}}) As r,
  If(!IsBlank(r.To) && CountRows(Filter(colTasks, Owner = r.O && Status <> "Done")) > 0,
    Office365Outlook.SendEmailV2(r.To,
      If(varHire.RequestType = "Termination", "Offboarding: ", "Onboarding: ") & varHire.Title & If(varHire.RequestType = "Termination", ", last day ", ", starts ") & Text(varHire.EffectiveDate, "mmm d", "en-US"),
      "<div style='font-family:Arial;font-size:13px;color:#202054'><h2>" & If(varHire.RequestType = "Termination", "Offboarding: ", "Onboarding: ") & varHire.Title & "</h2>" &
      "<p>" & If(varHire.RequestType = "Termination", "Last day: ", "Start date: ") & "<b>" & Text(varHire.EffectiveDate, "dddd, mmm d, yyyy", "en-US") & "</b></p>" &
      "<p>These tasks are assigned to " & If(r.O = "Manager", "you as the manager", r.O) & ":</p>" &
      "<table border='1' cellpadding='6' style='border-collapse:collapse;font-size:13px'><tr style='background:#EEEEF5'><th align='left'>Due</th><th align='left'>Task</th></tr>" &
      Concat(Sort(Filter(colTasks, Owner = r.O && Status <> "Done"), DueDate), "<tr><td>" & Text(DueDate, "mmm d", "en-US") & "</td><td>" & Title & "</td></tr>") &
      "</table><p>Please let HR know when each one is done. Thank you!</p></div>",
      {{Cc: User().Email}})));
Notify("Task lists sent", NotificationType.Success)'''
A(button("btnMailO",'"✉ Send task lists"',"Parent.Width - 220","76","200","40",mail,visible=LOADED,size=11))

# owner filter
A(ctrl("galOwnerO","Gallery@2.15.0",{"Items":'["All", "HR", "Manager", "EHS", "IT", "Overdue"]',"X":X0,"Y":"166","Width":"660","Height":"34","WrapCount":"6","TemplateSize":"34","TemplatePadding":"0","ShowScrollbar":"false","Visible":LOADED},variant="Vertical",children=[
  ctrl("btnOwnerO","Classic/Button@2.2.0",{"Text":'ThisItem.Value & "  " & If(ThisItem.Value = "All", CountRows(colTasks), ThisItem.Value = "Overdue", CountRows(Filter(colTasks, Status <> "Done" && DueDate < Today())), CountRows(Filter(colTasks, Owner = ThisItem.Value && Status <> "Done")))',
   "X":"0","Y":"0","Width":"Parent.TemplateWidth - 6","Height":"30","Size":"9",
   "Fill":f'If(Coalesce(varOwnerO, "All") = ThisItem.Value, {NAVY}, {LIGHT})',"Color":f'If(Coalesce(varOwnerO, "All") = ThisItem.Value, Color.White, {NAVY})',
   "HoverFill":'ColorValue("#C9C9D6")',"BorderThickness":"0","OnSelect":"Set(varOwnerO, ThisItem.Value)",**pill(15)},indent=6)]))

toggle='''With({d: ThisItem.Status <> "Done"},
  Patch(OnboardingTasks, LookUp(OnboardingTasks, ID = ThisItem.ID), {Status: If(d, "Done", "Pending"), DoneBy: If(d, User().FullName, ""), DoneOn: If(d, Today(), Blank())});
  Patch(colTasks, ThisItem, {Status: If(d, "Done", "Pending"), DoneBy: If(d, User().FullName, ""), DoneOn: If(d, Today(), Blank())}))'''
OVER='ThisItem.Status <> "Done" && ThisItem.DueDate < Today()'
A(ctrl("galTasksO","Gallery@2.15.0",{"Items":'Sort(Sort(Filter(colTasks, Switch(Coalesce(varOwnerO, "All"), "All", true, "Overdue", Status <> "Done" && DueDate < Today(), Owner = varOwnerO)), DueDate), Phase)',
  "X":X0,"Y":"208","Width":W,"Height":"Parent.Height - 214","TemplateSize":"62","TemplatePadding":"0","ShowScrollbar":"true","Visible":LOADED},variant="Vertical",children=[
  ctrl("recTaskO","Rectangle@2.3.0",{"X":"0","Y":"0","Width":"Parent.TemplateWidth","Height":"Parent.TemplateHeight - 4","Fill":'If(ThisItem.Status = "Done", ColorValue("#F3F8F4"), Color.White)',"BorderColor":'ColorValue("#E3E3E3")',"BorderThickness":"1"},indent=6),
  ctrl("btnChkO","Classic/Button@2.2.0",{"Text":'If(ThisItem.Status = "Done", "✓", "")',"X":"14","Y":"14","Width":"30","Height":"30","Size":"14","FontWeight":"FontWeight.Bold",
    "Fill":'If(ThisItem.Status = "Done", ColorValue("#1E7B34"), Color.White)',"Color":"Color.White","HoverFill":'ColorValue("#C9C9D6")',
    "BorderColor":'If(ThisItem.Status = "Done", ColorValue("#1E7B34"), ColorValue("#87878F"))',"BorderThickness":"2","OnSelect":toggle,**pill(6)},indent=6),
  ctrl("lblTaskO","Label@2.5.1",{"OnSelect":"Select(btnChkO)","Text":"ThisItem.Title","X":"58","Y":"6","Width":"Parent.TemplateWidth - 200","Height":"26","Size":"11","FontWeight":"FontWeight.Semibold",
    "Strikethrough":'ThisItem.Status = "Done"',"Color":f'If(ThisItem.Status = "Done", {GREY}, {NAVY})'},indent=6),
  ctrl("lblTaskInfoO","Label@2.5.1",{"OnSelect":"Select(btnChkO)",
    "Text":'Mid(ThisItem.Phase, 4) & "  ·  Due " & Text(ThisItem.DueDate, "mmm d", "en-US") & If(' + OVER + ', " (overdue)", "") & If(ThisItem.Kind = "Document", "  ·  File in: " & ThisItem.FiledIn, "") & If(ThisItem.Status = "Done", "  ·  ✓ " & ThisItem.DoneBy & " " & Text(ThisItem.DoneOn, "mmm d", "en-US"), "")',
    "X":"58","Y":"30","Width":"Parent.TemplateWidth - 200","Height":"24","Size":"9","Color":f'If({OVER}, ColorValue("#B3261E"), {GREY})'},indent=6),
  ctrl("lblOwnerO","Label@2.5.1",{"Text":"ThisItem.Owner","X":"Parent.TemplateWidth - 120","Y":"17","Width":"100","Height":"24","Size":"9","Align":"Align.Center","FontWeight":"FontWeight.Bold","Color":"Color.White","Fill":OWNC},indent=6)]))

open('/home/user/claude/altas-bajas/Pantalla-Onboarding-COPIAR.txt','w').write("\n".join(out)+"\n")
