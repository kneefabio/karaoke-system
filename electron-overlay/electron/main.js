const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const WebSocket = require('ws');

let mainWindow;
let ws;
let backendUrl = 'ws://localhost:8001/ws/photos'; // Modificabile

function createWindow() {
  mainWindow = new BrowserWindow({
    fullscreen: true,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadFile('index.html');
  mainWindow.setIgnoreMouseEvents(true); // Click-through
  
  // Dev tools (commentare in produzione)
  // mainWindow.webContents.openDevTools();
}

function connectWebSocket() {
  console.log('Connecting to WebSocket:', backendUrl);
  
  ws = new WebSocket(backendUrl);

  ws.on('open', () => {
    console.log('✅ WebSocket connected!');
    mainWindow.webContents.send('websocket-status', 'connected');
  });

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      console.log('📸 New photo received:', message);
      
      if (message.type === 'new_photo') {
        mainWindow.webContents.send('new-photo', {
          filename: message.filename,
          path: message.path
        });
      }
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  });

  ws.on('close', () => {
    console.log('❌ WebSocket disconnected. Reconnecting in 5s...');
    mainWindow.webContents.send('websocket-status', 'disconnected');
    setTimeout(connectWebSocket, 5000);
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error.message);
  });
}

app.whenReady().then(() => {
  createWindow();
  
  // Connetti WebSocket dopo 2 secondi
  setTimeout(connectWebSocket, 2000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (ws) {
    ws.close();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC per configurazione
ipcMain.on('set-backend-url', (event, url) => {
  backendUrl = url;
  if (ws) {
    ws.close();
  }
  setTimeout(connectWebSocket, 1000);
});
