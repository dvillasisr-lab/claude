# People Requests (altas, bajas y cambios)

App de HR para mandar a IT las altas, bajas y cambios de personal, con todos los datos (puesto, departamento estándar, empresa, oficina, jefe, backup, job description, scope, skills, equipo).

- `PeopleRequests.xlsx`: plantilla para crear la lista de SharePoint **PeopleRequests** (Nuevo > Lista > Desde Excel).
  Columnas de texto largo (elegir "Varias líneas de texto"): JobDescription, Scope, Skills, Equipment, SystemsAccess, PreviousValues, AutoReply, Notes. EffectiveDate: Fecha.
- `Pantalla-PeopleRequests-COPIAR.txt`: pantalla para pegar con Cmd+V en una app de lienzo en blanco.
  Orígenes de datos necesarios: UsuariosdeOffice365, Office365Outlook, PeopleRequests, Organigrama.
- Cambiar el texto de `lblITR` por el correo de IT.
- Al enviar una alta o cambio, también actualiza la lista **Organigrama** (puesto, área, jefe, descripción, scope, skills, backup, location y fecha de ingreso), así el organigrama se llena solo.
- `build_screen.py`: genera el .txt (listas de departamentos, empresas, oficinas y equipo al inicio del script).

## Checklists de onboarding y offboarding
- `OnboardingTasks.xlsx`: plantilla para la lista **OnboardingTasks** (los documentos se guardan en físico; la lista solo registra si se recibió y dónde se archivó).
- `Pantalla-Onboarding-COPIAR.txt`: pegar en una pantalla nueva llamada **scrOnboarding** dentro de la app People Requests (agregar el origen de datos OnboardingTasks).
- `btnOnbR-COPIAR.txt`: botón para ir de People Requests a los checklists.
- Cambiar el texto de `lblEHSO` por el correo de EHS.
