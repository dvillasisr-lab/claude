#!/bin/bash
# Uso: rev.sh NNN  -> arma la lámina sola y la revisa con check.js
R=/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/rev
cd /home/user/claude/braze-analysis/scripts && python3 deck_v6_render.py --solo ../deck/v6/slides/b1/$1.json $R/$1.html >/dev/null
cd /home/user/claude/braze-analysis/deck/v6/tools && NODE_PATH=/opt/node-tools/node_modules node check.js $R/$1.html $R/$1.png
