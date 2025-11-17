#!/bin/bash

echo "========================================"
echo "  Karaoke Photo Overlay - Avvio"
echo "========================================"
echo ""
echo "Avvio dell'overlay in corso..."
echo ""
echo "NOTA: Se ricevi errori, usa './install-and-start.sh'"
echo "      per installare prima le dipendenze."
echo ""

cd "$(dirname "$0")"
yarn start
