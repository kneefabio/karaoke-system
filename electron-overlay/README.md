# 🎤 Karaoke Photo Overlay - Guida Installazione

## 📋 Prerequisiti
- **Node.js** (versione 16 o superiore) - [Scarica qui](https://nodejs.org/)
- **Yarn** (opzionale, ma consigliato) - Installazione: `npm install -g yarn`

---

## 🚀 Installazione e Avvio

### OPZIONE 1: Avvio Veloce (con dipendenze già installate)

Se stai copiando questa cartella da un ambiente dove le dipendenze sono già installate:

**Windows:**
1. Doppio click su `start-overlay.bat`
2. L'overlay si avvierà in modalità fullscreen trasparente

**Mac/Linux:**
```bash
chmod +x start-overlay.sh
./start-overlay.sh
```

---

### OPZIONE 2: Installazione da Zero

Se è la prima volta o mancano le dipendenze:

#### Windows:
1. Doppio click su `install-and-start.bat`
2. Aspetta l'installazione delle dipendenze (1-2 minuti)
3. L'overlay si avvierà automaticamente

#### Mac/Linux:
```bash
chmod +x install-and-start.sh
./install-and-start.sh
```

---

## ⚙️ Configurazione

### Prima Apertura:
1. L'overlay si apre in **fullscreen trasparente**
2. Premi **C** per aprire il pannello di configurazione
3. **Inserisci il tuo Username Admin** (es: `admin1`, `testadmin`)
4. Verifica il Backend URL (default: `ws://127.0.0.1:8001/ws/photos`)
5. Clicca **Salva**

### ⚠️ IMPORTANTE:
- Devi inserire lo stesso **username** che usi per fare login nell'admin dashboard
- Solo le foto della tua serata appariranno sull'overlay
- Se non inserisci l'username, vedrai le foto di tutti gli admin!

---

## 🎮 Comandi Tastiera

- **C** = Apri/Chiudi Configurazione
- **H** = Nascondi/Mostra Barra di Controllo
- **T** = Test (debug)
- **Q** = Chiudi Overlay

## 🖱️ Spostare l'Overlay

- **Trascina la barra superiore** per spostare la finestra su un altro schermo
- Usa il pulsante **➖** per nascondere la barra quando non serve
- Premi **H** per mostrare/nascondere velocemente la barra

---

## 🔧 Risoluzione Problemi

### L'overlay non si connette:
1. Verifica che il backend sia avviato
2. Controlla l'URL del backend (premi C)
3. Verifica il firewall di Windows

### Non vedo le mie foto:
1. Premi **C** e verifica di aver inserito il tuo username admin
2. Controlla che il backend URL sia corretto
3. Guarda la console per i log di filtraggio

### Come chiudere l'overlay:
- Premi **Q** e conferma
- Oppure usa Alt+F4 (Windows) / Cmd+Q (Mac)

---

## 📦 Build Eseguibile (Opzionale)

Per creare un file .exe distribuibile:

```bash
yarn run build
```

L'eseguibile sarà in `dist/`

---

## 🎯 Come Usare con il Sistema Karaoke

1. **Admin Dashboard** → Vai in "Foto Serate"
2. Crea una nuova serata
3. Appuntati l'**ID Serata** (evidenziato in verde)
4. **Avvia l'Overlay sul PC** (questo overlay)
5. Premi **C** e inserisci il tuo **username admin**
6. Le foto caricate dalla camera app appariranno automaticamente!

---

## 📱 Informazioni Tecniche

- **Backend WebSocket**: Comunica in tempo reale con il server
- **Filtraggio**: Solo foto del tuo admin vengono mostrate
- **Animazioni**: Random per ogni foto (8 entrate + 7 uscite)
- **Posizioni**: 8 posizioni diverse sullo schermo
- **Trasparenza**: Click-through, non interferisce con altre app

---

## 💡 Suggerimenti

- Usa un secondo monitor per l'overlay
- Proietta lo schermo con l'overlay sul muro/schermo principale
- Le foto appaiono per 5 secondi (configurabile nella dashboard)
- L'overlay è sempre in primo piano

---

🎉 **Buon divertimento con le tue serate karaoke!**
