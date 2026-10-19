import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { createHashRouter, Outlet, RouterProvider, ScrollRestoration, useLocation } from 'react-router'
import './index.css'
import { Navigasi, Toaster, terapkanTema, useTemaAktif } from './components'
import { useApp } from './store'
import { Beranda, MiripDaftar, MiripDetail, Pelajaran, Peta } from './screens/belajar'
import { LayarLatihan } from './screens/latihan'
import { BacaSurah, DaftarSurah } from './screens/mushaf'
import { Pengenalan, Saya, Studi, Sus, Tes } from './screens/saya'

const TAB = ['/', '/peta', '/mushaf', '/saya']

function Kerangka() {
  const { pengaturan, catat } = useApp()
  const { pathname } = useLocation()
  useEffect(() => { document.documentElement.style.setProperty('--skala', String(pengaturan.skalaTeks)) }, [pengaturan.skalaTeks])
  useEffect(() => { catat('buka', undefined, pathname) }, [pathname, catat])
  const tema = useTemaAktif()
  useEffect(() => terapkanTema(tema), [tema])
  if (!pengaturan.onboarding) return <Pengenalan />
  const tab = TAB.includes(pathname)
  return (
    <div className={`min-h-dvh lg:pl-72 ${tab ? 'ada-tab' : ''}`}>
      <Outlet />
      <Navigasi tampilBawah={tab} />
      <Toaster />
      <ScrollRestoration />
    </div>
  )
}

// Hash router: jalan di hosting statis mana pun dan di WebView Capacitor tanpa konfigurasi server.
const router = createHashRouter([
  {
    element: <Kerangka />,
    children: [
      { path: '/', element: <Beranda /> },
      { path: '/huruf/:id/:langkah?', element: <Pelajaran /> },
      { path: '/latihan/:id', element: <LayarLatihan /> },
      { path: '/peta', element: <Peta /> },
      { path: '/mirip', element: <MiripDaftar /> },
      { path: '/mirip/:i', element: <MiripDetail /> },
      { path: '/mushaf', element: <DaftarSurah /> },
      { path: '/mushaf/:n', element: <BacaSurah /> },
      { path: '/saya', element: <Saya /> },
      { path: '/saya/studi', element: <Studi /> },
      { path: '/tes/:fase', element: <Tes /> },
      { path: '/sus', element: <Sus /> },
      { path: '*', element: <Beranda /> },
    ],
  },
])

if (!(window as { Capacitor?: { isNativePlatform?: () => boolean } }).Capacitor?.isNativePlatform?.()) {
  import('virtual:pwa-register').then((m) => m.registerSW({ immediate: true }))
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
