import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  // Path relatif supaya build yang sama jalan di hosting, subfolder, dan WebView Capacitor.
  base: './',
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      // Didaftarkan manual di main.tsx: tidak dipakai di APK (aset sudah dibundel).
      injectRegister: false,
      includeAssets: ['icon.svg', 'data/TANZIL_LICENSE.txt'],
      manifest: {
        name: 'Makhraj: belajar huruf dari tempat keluarnya',
        short_name: 'Makhraj',
        description: 'Aplikasi tahsin berbasis visualisasi makhraj dan rujukan guru bersanad.',
        lang: 'id',
        theme_color: '#0F5E5E',
        background_color: '#FBF8F2',
        display: 'standalone',
        start_url: './',
        icons: [{ src: 'icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any maskable' }],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,woff2,json,txt}'],
        // quran.json dan id.json sekitar 1,2-1,4 MB.
        maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
        // Video YouTube tidak boleh di-cache (Kebijakan YouTube API III.E.1).
        navigateFallbackDenylist: [/^\/api/],
      },
    }),
  ],
})
