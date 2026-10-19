#!/bin/bash
# Uso: rev.sh NNN  -> corre el script sNNN.py, arma la lámina sola y la revisa con check.js
set -e
N=$1
R=/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/rev
mkdir -p $R
cd /home/user/claude/braze-analysis/deck/v6/slides/b2/src
[ -f s$N.py ] && python3 s$N.py 2>&1 | grep -v Warning | tail -${TAILN:-30}
cd /home/user/claude/braze-analysis/scripts && python3 deck_v6_render.py --solo ../deck/v6/slides/b2/$N.json $R/$N.html >/dev/null
cd /home/user/claude/braze-analysis/deck/v6/tools && NODE_PATH=/opt/node-tools/node_modules node check.js $R/$N.html $R/$N.png
python3 /home/user/claude/braze-analysis/deck/v6/tools/lint.py /home/user/claude/braze-analysis/deck/v6/slides/b2/$N.json
