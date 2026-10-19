"""Campañas detrás de cada semana: E1 con primer y último envío de E2, campañas que duran 10 días o menos."""
import re, pandas as pd
from kit import D, team
def one_shot():
    e1 = pd.read_csv(D + 'e1_comunicacion_mes_canal.csv'); e2 = pd.read_csv(D + 'e2_catalogo.csv')
    e1 = e1[e1.envios > 0].copy(); e1['T'] = e1.team.map(team)
    e1 = e1.merge(e2[['communication_id', 'first_sent', 'last_sent']], on='communication_id', how='left')
    e1['m'] = e1.mes.str[:7]
    e1['fs'] = pd.to_datetime(e1.first_sent, errors='coerce', utc=True).dt.tz_localize(None)
    e1['ls'] = pd.to_datetime(e1.last_sent, errors='coerce', utc=True).dt.tz_localize(None)
    e1['span'] = (e1.ls - e1.fs).dt.days
    one = e1[(e1.span <= 10) & (e1.fs.dt.strftime('%Y-%m') == e1.m)].copy()
    one['wk'] = (one.fs.dt.normalize() - pd.to_timedelta(one.fs.dt.weekday, unit='D')).dt.strftime('%Y-%m-%d')
    return e1, one
