import sys
src = open('scripts/build_sheets_v4.py').read().split('\n')[:441]
ns = {'__name__': 'x'}
sys.argv = ['x', '--lo-test']
exec('\n'.join(src), ns)
camp = ns['camp']; camp.to_pickle('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/camp.pkl')
ns['g1'].to_pickle('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/g1.pkl')
ns['catp'].to_pickle('/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/v6parts/p6work/catp.pkl')
print(len(camp)); print(camp.accion.value_counts())
print('ahorro_mes_ent', camp.ahorro_mes_ent.sum(), 'env', camp.ahorro_mes_env.sum(), 'msgs', camp.msgs_ahorro.sum(), 'costo_mes_ent', camp.costo_mes_ent.sum(), 'msgs_mes', camp.msgs_mes.sum())
print(camp.groupby('equipo').ahorro_mes_ent.sum())
