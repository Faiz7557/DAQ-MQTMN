import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'

// Lewati layar pengenalan: anggap pengguna sudah pernah membuka aplikasi.
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    if (!localStorage.getItem('makhraj-v1'))
      localStorage.setItem('makhraj-v1', JSON.stringify({ state: { pengaturan: { onboarding: true, tampilkanHari: true, skalaTeks: 1, sumberVideo: 'andalasy', studi: null } }, version: 0 }))
  })
})

const RUTE = ['/', '/peta', '/huruf/haa', '/huruf/haa/1', '/huruf/haa/2', '/huruf/haa/3', '/huruf/haa/4',
  '/mirip/0', '/mushaf', '/mushaf/1?huruf=haa', '/saya', '/saya/studi']

async function buka(page: Page, rute: string) {
  await page.goto('#' + rute)
  await page.waitForLoadState('networkidle')
}

// WCAG 2.2 A/AA (Lampiran 11 proposal). Pemutar YouTube milik pihak ketiga tidak ikut diaudit.
for (const rute of RUTE) {
  test(`aksesibilitas ${rute}`, async ({ page }) => {
    await buka(page, rute)
    const hasil = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .exclude('iframe')
      .analyze()
    const berat = hasil.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical')
    expect(berat.map((v) => `${v.id}: ${v.help} (${v.nodes.length} elemen)`)).toEqual([])
  })
}

test('rekam suara tersimpan di IndexedDB dan muncul di daftar', async ({ page }) => {
  await buka(page, '/latihan/haa')
  await page.getByRole('button', { name: 'Mulai merekam' }).click()
  await page.waitForTimeout(1500)
  await page.getByRole('button', { name: 'Berhenti merekam' }).click()
  await expect(page.getByText('Rekaman saya')).toBeVisible()
  // Penyimpanan ke IndexedDB berjalan async setelah rekaman berhenti.
  await expect.poll(() => page.evaluate(() => new Promise<number>((ok, gagal) => {
    const r = indexedDB.open('makhraj')
    r.onerror = () => gagal(r.error)
    r.onsuccess = () => {
      const q = r.result.transaction('rekaman').objectStore('rekaman').count()
      q.onsuccess = () => ok(q.result)
      q.onerror = () => gagal(q.error)
    }
  })), { timeout: 8000 }).toBeGreaterThan(0)
})

test('cermin kamera menyala tanpa merekam video', async ({ page }) => {
  await buka(page, '/latihan/haa')
  await page.getByRole('button', { name: /cermin/i }).first().click()
  await expect(page.getByLabel('Cermin kamera depan')).toBeVisible()
  await expect(page.getByText('Cermin · tidak direkam')).toBeVisible()
})
