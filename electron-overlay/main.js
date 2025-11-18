const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const https = require('https');
const http = require('http');
const WebSocket = require('ws');
const os = require('os');

let mainWindow;
let ws;
let backendUrl = ''; // Lasciare vuoto - da configurare al primo avvio
let backendHttpUrl = ''; // URL HTTP per scaricare le foto
let adminUsername = ''; // Username admin da filtrare

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: false, // Mostra in taskbar per gestirlo meglio
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadFile('index.html');
  
  // NON usare setIgnoreMouseEvents - deve essere trascinabile!
  // Il click-through sarà gestito solo per il contenitore foto
  
  // Dev tools (commentare in produzione)
  // mainWindow.webContents.openDevTools();
}

function connectWebSocket() {
  if (!backendUrl) {
    console.log('⚠️  Backend URL not configured. Press C to configure.');
    mainWindow.webContents.send('websocket-status', 'disconnected');
    return;
  }
  
  console.log('Connecting to WebSocket:', backendUrl);
  
  ws = new WebSocket(backendUrl);

  ws.on('open', () => {
    console.log('✅ WebSocket connected!');
    mainWindow.webContents.send('websocket-status', 'connected');
  });

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      console.log('📸 Photo received:', message);
      
      if (message.type === 'new_photo') {
        // Filtra solo foto del proprio admin
        if (adminUsername && message.admin_username !== adminUsername) {
          console.log(`⏭️  Skipping photo from ${message.admin_username} (filtering for ${adminUsername})`);
          return;
        }
        
        console.log(`✅ Showing photo from ${message.admin_username}`);
        
        // Costruisci URL completo della foto
        const photoUrl = `${backendHttpUrl}${message.url}`;
        console.log(`📷 Photo URL: ${photoUrl}`);
        
        mainWindow.webContents.send('new-photo', {
          filename: message.filename,
          url: photoUrl
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
  
  // Deriva HTTP URL dal WebSocket URL
  // ws://localhost:8001/ws/photos -> http://localhost:8001
  // wss://backend.com/ws/photos -> https://backend.com
  if (url.startsWith('wss://')) {
    backendHttpUrl = url.replace('wss://', 'https://').replace('/ws/photos', '');
  } else if (url.startsWith('ws://')) {
    backendHttpUrl = url.replace('ws://', 'http://').replace('/ws/photos', '');
  }
  
  console.log(`🌐 Backend HTTP URL: ${backendHttpUrl}`);
  
  if (ws) {
    ws.close();
  }
  setTimeout(connectWebSocket, 1000);
});

ipcMain.on('set-admin-username', (event, username) => {
  adminUsername = username;
  console.log(`🎯 Filtering photos for admin: ${adminUsername}`);
  event.sender.send('config-saved', { admin_username: adminUsername });
});
