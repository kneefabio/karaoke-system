#!/bin/bash

echo "========================================"
echo "  Karaoke Photo Overlay"
echo "  Installazione e Avvio"
echo "========================================"
echo ""
echo "Controllo Node.js..."

if ! command -v node &> /dev/null; then
    echo "ERRORE: Node.js non trovato!"
    echo ""
    echo "Installazione Node.js:"
    echo "  Mac: brew install node"
    echo "  Linux: sudo apt install nodejs npm"
    echo ""
    exit 1
fi

echo "Node.js trovato: OK"
node --version
echo ""

cd "$(dirname "$0")"

echo "Installazione dipendenze..."
echo "Questo potrebbe richiedere 1-2 minuti..."
echo ""

yarn install
if [ $? -ne 0 ]; then
    echo ""
    echo "ERRORE durante l'installazione!"
    echo "Prova con: npm install"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "  Installazione completata!"
echo "========================================"
echo ""
echo "Avvio overlay..."
echo ""
echo "COMANDI:"
echo "  C = Configurazione"
echo "  Q = Chiudi"
echo ""
echo "RICORDA: Inserisci il tuo username admin nella configurazione!"
echo ""

yarn start
