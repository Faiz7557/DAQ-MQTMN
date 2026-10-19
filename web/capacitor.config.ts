import type { CapacitorConfig } from '@capacitor/cli'

// Jangan set server.url/hostname: dilaporkan mematikan getUserMedia (mikrofon/kamera) di WebView.
const config: CapacitorConfig = {
  appId: 'id.makhraj.app',
  appName: 'Makhraj',
  webDir: 'dist',
}

export default config
