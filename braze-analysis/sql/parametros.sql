-- Parámetros del análisis. Cambiar aquí y todo lo demás los usa.
-- Dialecto: ANSI. En Databricks cambiar las comillas dobles de "date" y "group" por acentos graves.

-- Periodo
--   fecha_inicio = DATE '2026-01-01'
--   fecha_fin    = DATE '2026-09-30'
--   meses: enero a septiembre 2026, los 9 completos
--   semanas: solo completas (lunes a domingo), del 2026-01-05 al 2026-09-27, 38 semanas
--            la semana del 2025-12-29 y la del 2026-09-28 se excluyen por tener solo 3 dias dentro del periodo
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
