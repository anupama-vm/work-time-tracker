const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getLogs: () => ipcRenderer.invoke('get-logs')
});
