#!/bin/bash
# Uso: check.sh 066 [067 ...]  -> arma cada lámina sola y la revisa con check.js (PNG en scratchpad/rev)
REV=/tmp/claude-0/-home-user-claude/e114ba4f-39d4-57f8-9f24-b0f0c0cbef51/scratchpad/rev
mkdir -p $REV
for n in "$@"; do
  cd /home/user/claude/braze-analysis/scripts && python3 deck_v6_render.py --solo ../deck/v6/slides/b7/$n.json $REV/$n.html >/dev/null
  cd /home/user/claude/braze-analysis/deck/v6/tools && echo "[$n] $(NODE_PATH=/opt/node-tools/node_modules node check.js $REV/$n.html $REV/$n.png)"
done
