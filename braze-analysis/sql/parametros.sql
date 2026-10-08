-- Parámetros del análisis. Cambiar aquí y todo lo demás los usa.
-- Dialecto: ANSI. En Databricks cambiar las comillas dobles de "date" y "group" por acentos graves.

-- Periodo
--   fecha_inicio = DATE '2026-01-01'
--   fecha_fin    = DATE '2026-09-30'
--   octubre 2026 se reporta aparte como mes parcial

-- Tarifas MXN por mensaje (dato del usuario, 8 oct 2026)
--   email     0.05
--   whatsapp  1.00
--   push      0.00
--   in_app    0.00
--   banner    0.00
--   costo fijo Braze mensual: pendiente

-- Umbrales
--   presion: 5 mensajes por semana (sin contar operativos)
--   zombi:   sin envio en 90 dias y no archivada
--   solape:  3 o mas comunicaciones el mismo dia al mismo usuario
