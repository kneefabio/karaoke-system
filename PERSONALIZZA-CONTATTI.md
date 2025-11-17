# 📞 PERSONALIZZA I CONTATTI ASSISTENZA

## ⚠️ IMPORTANTE: Sostituisci i Placeholder!

I contatti nella pagina "Licenza Mancante" sono **PLACEHOLDER** e devono essere sostituiti con i tuoi dati reali.

---

## 📝 DOVE MODIFICARE

**File:** `frontend/src/pages/NoLicensePage.jsx`

**Linee da modificare:** Cerca questa sezione (~linea 90-130)

---

## 🔧 COSA CAMBIARE

### 1. EMAIL
```jsx
// CERCA:
<a href="mailto:support@karaokeapp.com" ...>
  <div className="text-sm text-gray-600">support@karaokeapp.com</div>
</a>

// SOSTITUISCI CON:
<a href="mailto:TUA_EMAIL@dominio.com" ...>
  <div className="text-sm text-gray-600">TUA_EMAIL@dominio.com</div>
</a>
```

**Esempio:**
```jsx
href="mailto:assistenza@fabiokaraoke.it"
<div className="text-sm text-gray-600">assistenza@fabiokaraoke.it</div>
```

---

### 2. TELEFONO
```jsx
// CERCA:
<a href="tel:+393001234567" ...>
  <div className="text-sm text-gray-600">+39 300 123 4567</div>
</a>

// SOSTITUISCI CON:
<a href="tel:+39TUONUMERO" ...>
  <div className="text-sm text-gray-600">+39 XXX XXX XXXX</div>
</a>
```

**Esempio:**
```jsx
href="tel:+393331234567"
<div className="text-sm text-gray-600">+39 333 123 4567</div>
```

---

### 3. WHATSAPP
```jsx
// CERCA:
<a href="https://wa.me/393001234567" ...>
  <div className="text-sm text-gray-600">+39 300 123 4567</div>
</a>

// SOSTITUISCI CON:
<a href="https://wa.me/39TUONUMERO" ...>
  <div className="text-sm text-gray-600">+39 XXX XXX XXXX</div>
</a>
```

**Esempio:**
```jsx
href="https://wa.me/393331234567"
<div className="text-sm text-gray-600">+39 333 123 4567</div>
```

**NOTA:** Il link WhatsApp usa il formato internazionale SENZA spazi o simboli `+`
- ✅ Corretto: `https://wa.me/393331234567`
- ❌ Sbagliato: `https://wa.me/+39 333 123 4567`

---

### 4. PREZZI LICENZE (Opzionale)

Se vuoi cambiare i prezzi mostrati:

```jsx
// CERCA (linea ~160):
<div className="grid grid-cols-3 gap-3 text-center text-sm">
  <div className="bg-white p-3 rounded">
    <div className="font-bold text-purple-600">1 Sera</div>
    <div className="text-xs text-gray-600">€14.90</div>
  </div>
  <div className="bg-white p-3 rounded">
    <div className="font-bold text-purple-600">1 Mese</div>
    <div className="text-xs text-gray-600">€39.90</div>
  </div>
  <div className="bg-white p-3 rounded">
    <div className="font-bold text-purple-600">1 Anno</div>
    <div className="text-xs text-gray-600">€129.90</div>
  </div>
</div>
```

Modifica i prezzi con i tuoi.

---

## 🛠️ COME APPLICARE LE MODIFICHE

### Metodo 1: Editor di Codice (RACCOMANDATO)
1. Apri `frontend/src/pages/NoLicensePage.jsx`
2. Cerca `support@karaokeapp.com`
3. Sostituisci con la tua email
4. Cerca `+393001234567`
5. Sostituisci con il tuo numero
6. Salva il file

### Metodo 2: Cerca e Sostituisci (VSCode)
1. Apri il file
2. Premi `Ctrl+H` (Windows) o `Cmd+H` (Mac)
3. Cerca: `support@karaokeapp.com`
4. Sostituisci con: `tua_email@dominio.com`
5. "Sostituisci Tutto"
6. Ripeti per il numero di telefono

---

## ✅ CHECKLIST MODIFICHE

Prima del deploy, verifica:

- [ ] Email sostituita (3 volte: mailto, text display)
- [ ] Telefono sostituito (2 volte: tel link, text display)
- [ ] WhatsApp sostituito (2 volte: wa.me link, text display)
- [ ] Link WhatsApp senza spazi o `+`
- [ ] Prezzi aggiornati (opzionale)
- [ ] Test link cliccando in locale

---

## 🧪 COME TESTARE

### Test Email:
1. Apri la pagina `/no-license`
2. Clicca sull'email
3. Dovrebbe aprire il client email con il TUO indirizzo

### Test Telefono:
1. Apri da mobile
2. Clicca sul numero
3. Dovrebbe aprire l'app telefono con il TUO numero

### Test WhatsApp:
1. Clicca sul link WhatsApp
2. Dovrebbe aprire WhatsApp con il TUO numero
3. Verifica che il numero sia corretto

---

## 💡 SUGGERIMENTI

### Email Professionale:
- ✅ assistenza@tuodominio.it
- ✅ support@karaokelicenze.it
- ✅ info@tuokaraoke.com
- ❌ mario.rossi@gmail.com (troppo personale)

### Numero di Telefono:
- Usa un numero dedicato al business
- Se possibile, numero con WhatsApp Business
- Considera un numero verde (800...)

### Messaggio WhatsApp Pre-compilato (Opzionale):
```jsx
href="https://wa.me/393331234567?text=Ciao,%20ho%20bisogno%20di%20assistenza%20per%20la%20licenza%20karaoke"
```

Questo apre WhatsApp con un messaggio già scritto!

---

## 🚀 DOPO LE MODIFICHE

1. Salva il file
2. Testa in locale: `yarn start`
3. Vai su `http://localhost:3000/no-license`
4. Verifica che tutto funzioni
5. Carica su GitHub
6. Deploy su Netlify

---

**RICORDA:** Questi contatti sono la prima impressione del tuo business. 
Assicurati che siano professionali e sempre raggiungibili! 📞

---

**File da modificare:** `/app/frontend/src/pages/NoLicensePage.jsx`
