import { defineConfig } from '@playwright/test'

// Tes e2e di peramban sungguhan (Edge terpasang; tidak perlu `playwright install`).
// Mikrofon dan kamera memakai perangkat palsu Chromium, jadi alur rekam bisa diuji tanpa manusia.
export default defineConfig({
  testDir: 'e2e',
  testMatch: '*.e2e.ts', // bukan *.test.ts, supaya tidak diambil Vitest
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'e2e-report' }]],
  use: {
    baseURL: 'http://127.0.0.1:8078/',
    channel: 'msedge',
    viewport: { width: 390, height: 844 },
    permissions: ['microphone', 'camera'],
    launchOptions: { args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'] },
    serviceWorkers: 'block',
  },
  webServer: {
    command: 'npm run preview -- --host 127.0.0.1 --strictPort',
    url: 'http://127.0.0.1:8078/',
    reuseExistingServer: true,
  },
})
