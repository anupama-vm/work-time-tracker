const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
let trackerProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 400,
    height: 300,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();
});

ipcMain.handle('signup', (event, email) => {
  console.log(`User signed up with email: ${email}`);
  return { success: true };
});

ipcMain.handle('start-tracker', () => {
  if (!trackerProcess) {
    const { spawn } = require('child_process');
    trackerProcess = spawn('python', ['../tracker/main.py']);
    console.log('Tracker started');
    trackerProcess.stdout.on('data', (data) => console.log(`Tracker: ${data}`));
    trackerProcess.stderr.on('data', (data) => console.error(`Tracker Error: ${data}`));
  }
  return { success: true };
});

ipcMain.handle('stop-tracker', () => {
  if (trackerProcess) {
    trackerProcess.kill();
    trackerProcess = null;
    console.log('Tracker stopped');
  }
  return { success: true };
});
