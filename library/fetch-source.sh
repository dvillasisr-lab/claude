#!/bin/bash
# Clones a plugin source repo on demand so its skills/agents can be read without enabling the plugin.
# Usage: library/fetch-source.sh <superpowers|ecc|mattpocock|marketing|caveman|voltagent|all>
set -euo pipefail
DEST=/tmp/skill-sources
declare -A REPOS=(
  [superpowers]=obra/superpowers
  [ecc]=affaan-m/ECC
  [mattpocock]=mattpocock/skills
  [marketing]=coreyhaines31/marketingskills
  [caveman]=JuliusBrussee/caveman
  [voltagent]=VoltAgent/awesome-claude-code-subagents
)
names=("$@"); [ "${1:-}" = all ] && names=("${!REPOS[@]}")
mkdir -p "$DEST"
for n in "${names[@]}"; do
  [ -d "$DEST/$n" ] || git clone -q --depth 1 "https://github.com/${REPOS[$n]}.git" "$DEST/$n"
  echo "$DEST/$n"
done
