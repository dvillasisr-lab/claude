# Organigrama Sussek (Power Apps)

Archivos para reconstruir la app:

- `App-OnStart-COPIAR.txt`: fórmula de App.OnStart (formato español, con `;` y `;;`). Cambiar `CORREO_DE_CHRIS@sussek.com` por el correo real del CEO.
- `Pantalla-Organigrama-COPIAR.txt`: pegar en una pantalla en blanco llamada `scrMain`.
- `Pantalla-Celebrations-COPIAR.txt`: pantalla de nuevos ingresos y aniversarios. **Retirada por ahora** (Microsoft 365 no tiene fechas de ingreso). Para volver a usarla: crear pantalla `scrCelebrations`, pegar este archivo y agregar de nuevo el botón del menú en `scrMain`.

Conexiones requeridas: SharePoint (lista `Organigrama`), `UsuariosdeOffice365`, `Office365Outlook`.
Configuración: Diseño de la aplicación adaptable, límite de filas 2000, `App.MinScreenWidth = 320`.
