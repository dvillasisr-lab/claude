#!/bin/bash
# Construye deck/v6/pptx/DECK_v6.pptx desde DECK_v6.html. Requiere pptxgenjs en NODE_PATH.
set -e
cd "$(dirname "$0")/../../.."
node deck/v6/tools/html2pptx.js deck/v6/DECK_v6.html deck/v6/pptx/DECK_v6.pptx
python3 deck/v6/tools/pptx_ocultar.py deck/v6/pptx/DECK_v6.pptx
rm -f deck/v6/pptx/DECK_v6.pptx.ocultas.json
