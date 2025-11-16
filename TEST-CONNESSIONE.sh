#!/bin/bash

echo "========================================="
echo "  TEST CONNESSIONE KARAOKE SYSTEM"
echo "========================================="
echo ""

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URLs
BACKEND_URL="https://karaoke-backend-g48m.onrender.com"
FRONTEND_URL="https://astounding-buttercream-5d9ab5.netlify.app"

echo "🔍 Test 1: Backend Health Check"
echo "URL: $BACKEND_URL/api/health"
echo ""

HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/api/health" 2>&1)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Backend è ONLINE${NC}"
    echo "Risposta: $BODY"
else
    echo -e "${RED}❌ Backend NON risponde${NC}"
    echo "HTTP Code: $HTTP_CODE"
    echo "Risposta: $BODY"
fi

echo ""
echo "========================================="
echo ""

echo "🔍 Test 2: Frontend Accessibility"
echo "URL: $FRONTEND_URL"
echo ""

FRONTEND_RESPONSE=$(curl -s -w "\n%{http_code}" "$FRONTEND_URL" 2>&1)
HTTP_CODE=$(echo "$FRONTEND_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend è ONLINE${NC}"
else
    echo -e "${RED}❌ Frontend NON risponde${NC}"
    echo "HTTP Code: $HTTP_CODE"
fi

echo ""
echo "========================================="
echo ""

echo "🔍 Test 3: Test Login Admin"
echo "POST: $BACKEND_URL/api/admin/login"
echo ""

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND_URL/api/admin/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' 2>&1)

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
BODY=$(echo "$LOGIN_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Login funziona correttamente${NC}"
    echo "Risposta: $BODY"
else
    echo -e "${RED}❌ Login NON funziona${NC}"
    echo "HTTP Code: $HTTP_CODE"
    echo "Risposta: $BODY"
    echo ""
    echo -e "${YELLOW}Possibili cause:${NC}"
    echo "1. Database non connesso"
    echo "2. CORS non configurato correttamente"
    echo "3. Variabili d'ambiente non configurate su Render"
fi

echo ""
echo "========================================="
echo ""

echo "📊 RIEPILOGO TEST"
echo ""
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo ""
echo "Per ulteriori informazioni, leggi:"
echo "  - CONFIGURAZIONE-RENDER-NETLIFY.md"
echo "  - ISTRUZIONI-FILE-ENV.md"
echo ""
echo "========================================="
