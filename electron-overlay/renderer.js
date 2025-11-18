const { ipcRenderer } = require('electron');
const fs = require('fs');

const statusEl = document.getElementById('status');
const statusText = document.getElementById('status-text');
const photoContainer = document.getElementById('photo-container');
const configPanel = document.getElementById('config');
const controlBar = document.getElementById('control-bar');

let displayTime = 5000; // Default 5 secondi
let barVisible = true;

// Animazioni disponibili
const entryAnimations = [
  'fadeIn',
  'slideInLeft',
  'slideInRight',
  'slideInTop',
  'slideInBottom',
  'bounceIn',
  'zoomIn',
  'rotateIn'
];

const exitAnimations = [
  'fadeOut',
  'slideOutLeft',
  'slideOutRight',
  'slideOutTop',
  'slideOutBottom',
  'zoomOut',
  'rotateOut'
];

// Posizioni possibili
const positions = [
  { top: '10%', left: '10%' },
  { top: '10%', right: '10%' },
  { bottom: '10%', left: '10%' },
  { bottom: '10%', right: '10%' },
  { top: '50%', left: '10%', transform: 'translateY(-50%)' },
  { top: '50%', right: '10%', transform: 'translateY(-50%)' },
  { top: '10%', left: '50%', transform: 'translateX(-50%)' },
  { bottom: '10%', left: '50%', transform: 'translateX(-50%)' }
];

// WebSocket status
ipcRenderer.on('websocket-status', (event, status) => {
  if (status === 'connected') {
    statusEl.className = 'status connected';
    statusText.textContent = '✓ Connected';
  } else {
    statusEl.className = 'status disconnected';
    statusText.textContent = '✗ Disconnected';
  }
});

// Nuova foto ricevuta
ipcRenderer.on('new-photo', (event, data) => {
  console.log('📸 Showing photo:', data.filename, 'from URL:', data.url);
  showPhoto(data.url);
});

function showPhoto(photoUrl) {
  console.log('🖼️  Loading photo from:', photoUrl);

  // Crea elemento img
  const img = document.createElement('img');
  img.src = photoUrl;  // URL HTTP invece di file://
  img.className = 'photo-overlay';
  
  // Gestisci errori di caricamento
  img.onerror = () => {
    console.error('❌ Failed to load photo:', photoUrl);
  };
  
  img.onload = () => {
    console.log('✅ Photo loaded successfully');
  };

  // Random position
  const position = positions[Math.floor(Math.random() * positions.length)];
  Object.assign(img.style, position);

  // Random entry animation
  const entryAnim = entryAnimations[Math.floor(Math.random() * entryAnimations.length)];
  img.style.animation = `${entryAnim} 0.8s ease-out`;

  // Aggiungi al container
  photoContainer.appendChild(img);

  // Rimuovi dopo displayTime
  setTimeout(() => {
    // Random exit animation
    const exitAnim = exitAnimations[Math.floor(Math.random() * exitAnimations.length)];
    img.style.animation = `${exitAnim} 0.8s ease-in`;

    // Rimuovi dopo animazione
    setTimeout(() => {
      photoContainer.removeChild(img);
    }, 800);
  }, displayTime);
}

// Control bar buttons
document.getElementById('minimize-btn').addEventListener('click', () => {
  barVisible = !barVisible;
  if (barVisible) {
    controlBar.classList.remove('hidden');
  } else {
    controlBar.classList.add('hidden');
  }
});

document.getElementById('config-btn').addEventListener('click', () => {
  configPanel.style.display = configPanel.style.display === 'none' ? 'block' : 'none';
});

document.getElementById('close-btn').addEventListener('click', () => {
  if (confirm('Chiudere l\'overlay?')) {
    window.close();
  }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // C = Config
  if (e.key === 'c' || e.key === 'C') {
    configPanel.style.display = configPanel.style.display === 'none' ? 'block' : 'none';
  }
  
  // Q = Quit
  if (e.key === 'q' || e.key === 'Q') {
    if (confirm('Chiudere l\'overlay?')) {
      window.close();
    }
  }

  // H = Hide/Show control bar
  if (e.key === 'h' || e.key === 'H') {
    barVisible = !barVisible;
    if (barVisible) {
      controlBar.classList.remove('hidden');
    } else {
      controlBar.classList.add('hidden');
    }
  }

  // T = Test photo
  if (e.key === 't' || e.key === 'T') {
    // Simula foto di test
    console.log('Test photo triggered');
    const testPath = '/app/Foto_Serate'; // Dummy per test
    // In realtà non mostrerà nulla perché non esiste, ma testa il flusso
  }
});

// Config save
document.getElementById('save-config').addEventListener('click', () => {
  const url = document.getElementById('backend-url').value;
  const username = document.getElementById('admin-username').value;
  
  if (!username) {
    alert('⚠️ Inserisci il tuo username admin per filtrare le foto!');
    return;
  }
  
  ipcRenderer.send('set-backend-url', url);
  ipcRenderer.send('set-admin-username', username);
  configPanel.style.display = 'none';
});

// Config saved confirmation
ipcRenderer.on('config-saved', (event, data) => {
  console.log('✅ Config saved:', data);
  alert(`Configurazione salvata!\nFiltraggio foto per: ${data.admin_username}`);
});

document.getElementById('close-config').addEventListener('click', () => {
  configPanel.style.display = 'none';
});

// Log di avvio
console.log('🎉 Karaoke Photo Overlay Started!');
console.log('📍 Press C for config');
console.log('📍 Press H to hide/show control bar');
console.log('📍 Press T for test');
console.log('📍 Press Q to quit');
console.log('💡 Drag the top bar to move to another screen');
