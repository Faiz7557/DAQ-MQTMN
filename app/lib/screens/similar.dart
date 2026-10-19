import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../theme.dart';
import '../widgets/common.dart';
import '../widgets/head_diagram.dart';

/// Daftar pasangan huruf yang sering tertukar.
class SimilarListScreen extends StatelessWidget {
  const SimilarListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
          children: [
            const Header('Huruf mirip'),
            const SizedBox(height: 12),
            const Text(
              'Pasangan huruf yang sering tertukar oleh pemula.',
              style: TextStyle(fontSize: 14, height: 1.5, color: C.grey),
            ),
            const SizedBox(height: 12),
            for (final (i, m) in materi.mirip.indexed) ...[
              Material(
                color: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(18),
                  side: const BorderSide(color: C.line),
                ),
                child: InkWell(
                  borderRadius: BorderRadius.circular(18),
                  onTap: () => context.push('/mirip/$i'),
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Row(
                      children: [
                        LetterTile(materi.hurufById(m.a).huruf, size: 44),
                        const SizedBox(width: 8),
                        LetterTile(materi.hurufById(m.b).huruf, size: 44, dashed: true),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${materi.hurufById(m.a).nama} dan ${materi.hurufById(m.b).nama}',
                                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
                              ),
                              Text(
                                m.kuis.isEmpty ? 'Penjelasan sedang divalidasi' : 'Penjelasan dan kuis',
                                style: const TextStyle(fontSize: 12, color: C.grey),
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.chevron_right, color: C.grey),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 10),
            ],
          ],
        ),
      ),
    );
  }
}

class SimilarScreen extends StatefulWidget {
  const SimilarScreen({super.key, required this.index});
  final int index;

  @override
  State<SimilarScreen> createState() => _SimilarScreenState();
}

class _SimilarScreenState extends State<SimilarScreen> {
  int _soal = 0;
  String? _jawab;

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final m = materi.mirip[widget.index];
    final a = materi.hurufById(m.a), b = materi.hurufById(m.b);
    final kuis = m.kuis.isEmpty ? null : m.kuis[_soal % m.kuis.length];

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
          children: [
            const Header('Huruf mirip'),
            const SizedBox(height: 14),
            Text(
              m.judul ?? '${a.nama} dan ${b.nama}',
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 4),
            Text(
              m.ringkas ?? 'Penjelasan perbedaan pasangan ini sedang disusun dan akan divalidasi pengajar tahsin.',
              style: const TextStyle(fontSize: 14, height: 1.5, color: C.grey),
            ),
            const SizedBox(height: 14),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: _Kartu(h: a, warna: C.teal),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _Kartu(h: b, warna: C.goldDark),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (kuis != null)
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(color: C.teal, borderRadius: BorderRadius.circular(24)),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Row(
                      children: [
                        const Expanded(
                          child: Text(
                            'Uji pemahaman',
                            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: Colors.white),
                          ),
                        ),
                        Text(
                          'Soal ${_soal % m.kuis.length + 1}/${m.kuis.length}',
                          style: const TextStyle(fontSize: 12, color: Color(0xFFCDE5E1)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(kuis.tanya, style: const TextStyle(fontSize: 14, height: 1.5, color: Colors.white)),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        for (final (i, h) in [a, b].indexed) ...[
                          if (i > 0) const SizedBox(width: 10),
                          Expanded(
                            child: _Jawab(
                              h: h,
                              jawab: _jawab,
                              benar: kuis.jawab,
                              onTap: () => setState(() => _jawab = h.id),
                            ),
                          ),
                        ],
                      ],
                    ),
                    if (_jawab != null) ...[
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(color: C.tealDark, borderRadius: BorderRadius.circular(12)),
                        child: Text(
                          _jawab == kuis.jawab
                              ? 'Benar! Jawabannya ${materi.hurufById(kuis.jawab).huruf}.'
                              : 'Belum tepat. Jawabannya ${materi.hurufById(kuis.jawab).huruf}; lihat lagi letak makhrajnya di atas.',
                          style: const TextStyle(fontSize: 14, height: 1.5, color: Colors.white),
                        ),
                      ),
                      const SizedBox(height: 10),
                      FilledButton(
                        onPressed: () => setState(() {
                          _soal++;
                          _jawab = null;
                        }),
                        style: FilledButton.styleFrom(backgroundColor: Colors.white, foregroundColor: C.teal),
                        child: const Text('Soal berikutnya'),
                      ),
                    ],
                  ],
                ),
              )
            else
              const Note(Text('Kuis untuk pasangan ini akan tersedia setelah materinya divalidasi.')),
          ],
        ),
      ),
    );
  }
}

class _Kartu extends StatelessWidget {
  const _Kartu({required this.h, required this.warna});
  final Huruf h;
  final Color warna;

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final area = materi.areaById(h.area);
    final p = h.pelajaran;
    final tenggorokan = h.area == 'halq';
    return Material(
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: const BorderSide(color: C.line),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () => context.push('/huruf/${h.id}'),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              Text(h.huruf, style: arab(44, color: warna, height: 1.3)),
              HeadDiagram(sorot: materi.sorotHuruf(h), view: tenggorokan ? kViewTenggorokan : kViewPenuh),
              const SizedBox(height: 8),
              Text(
                p?.namaTitik ?? area.nama,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 4),
              Text(
                area.arti,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 12, color: C.grey),
              ),
              if (p?.contoh != null) ...[
                const SizedBox(height: 6),
                Text(p!.contoh!.kata, style: arab(22, weight: FontWeight.w400)),
                Text(
                  '${p.contoh!.baca} · ${p.contoh!.arti}',
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 12, color: C.grey),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _Jawab extends StatelessWidget {
  const _Jawab({required this.h, required this.jawab, required this.benar, required this.onTap});
  final Huruf h;
  final String? jawab, benar;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final dipilih = jawab == h.id;
    final tampilBenar = jawab != null && h.id == benar;
    final salah = dipilih && h.id != benar;
    return Semantics(
      button: true,
      label: 'Jawab ${h.nama}',
      child: Material(
        color: tampilBenar ? Colors.white : (salah ? C.tealDark : C.teal),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: salah ? C.goldLight : Colors.white, width: 2),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: jawab == null ? onTap : null,
          child: SizedBox(
            height: 72,
            child: Center(
              child: Text(
                h.huruf,
                style: arab(36, color: tampilBenar ? C.teal : (salah ? C.goldLight : Colors.white), height: 1.2),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
