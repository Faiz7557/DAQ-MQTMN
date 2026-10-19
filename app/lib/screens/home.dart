import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../data/quran.dart';
import '../theme.dart';
import '../widgets/common.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final quran = context.read<Quran>();
    final prog = context.watch<Progress>();
    final next = materi.huruf.firstWhere((h) => !prog.sudah(h.id), orElse: () => materi.huruf.first);
    final area = materi.areaById(next.area);
    final dikuasai = materi.huruf.where((h) => prog.sudah(h.id)).toList();
    final total = materi.huruf.length;
    final last = quran.suras[prog.terakhirSurah - 1];

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 28, 20, 20),
      children: [
        Row(
          children: [
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("Assalamu'alaikum", style: TextStyle(fontSize: 13, color: C.grey)),
                  SizedBox(height: 4),
                  Text('Yuk lanjut belajar', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(color: C.goldLight, borderRadius: BorderRadius.circular(14)),
              child: Row(
                children: [
                  const Icon(Icons.local_fire_department_outlined, size: 16, color: C.goldDark),
                  const SizedBox(width: 6),
                  Text(
                    '${prog.streak} hari',
                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: C.goldDark),
                  ),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 18),
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(color: C.teal, borderRadius: BorderRadius.circular(24)),
          child: Row(
            children: [
              Container(
                width: 84,
                height: 84,
                alignment: Alignment.center,
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(20)),
                child: Text(next.huruf, style: arab(48, color: C.teal, height: 1.2)),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Pelajaran berikutnya · ${area.nama}',
                      style: const TextStyle(fontSize: 12, color: Color(0xFFCDE5E1)),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Huruf ${next.nama}',
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700, color: Colors.white),
                    ),
                    const SizedBox(height: 2),
                    Text(area.arti, style: const TextStyle(fontSize: 13, color: Color(0xFFDCEDEA))),
                    const SizedBox(height: 8),
                    FilledButton(
                      onPressed: () => context.push('/huruf/${next.id}'),
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: C.teal,
                        minimumSize: const Size(0, 40),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        textStyle: const TextStyle(fontFamily: 'Jakarta', fontWeight: FontWeight.w700),
                      ),
                      child: const Text('Mulai belajar'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 18),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: kCard,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Expanded(
                    child: Text('Huruf hijaiyah dikuasai', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700)),
                  ),
                  Text(
                    '${dikuasai.length} / $total',
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: C.teal),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: dikuasai.length / total,
                  minHeight: 8,
                  backgroundColor: const Color(0xFFEFE9DC),
                  color: C.teal,
                ),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  for (final h in dikuasai.take(7))
                    LetterTile(h.huruf, onTap: () => context.push('/huruf/${h.id}'), label: 'Ulangi huruf ${h.nama}'),
                  LetterTile(
                    next.huruf,
                    dashed: true,
                    onTap: () => context.push('/huruf/${next.id}'),
                    label: 'Huruf berikutnya',
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 18),
        const SectionTitle('Menu belajar'),
        const SizedBox(height: 10),
        for (final pair in [
          [
            _Menu(
              Icons.map_outlined,
              'Peta Makhraj',
              '5 area, ${materi.huruf.length} huruf',
              () => context.go('/peta'),
            ),
            _Menu(Icons.swap_horiz, 'Huruf Mirip', '6 pasangan, mis. ح dan ه', () => context.push('/mirip')),
          ],
          [
            _Menu(Icons.mic_none, 'Rekam Bacaan', 'Bandingkan dengan guru', () => context.push('/latihan/${next.id}')),
            _Menu(Icons.menu_book_outlined, 'Mushaf', 'Lanjut ${last.tname}', () => context.push('/mushaf/${last.n}')),
          ],
        ])
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: IntrinsicHeight(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(child: pair[0]),
                  const SizedBox(width: 10),
                  Expanded(child: pair[1]),
                ],
              ),
            ),
          ),
      ],
    );
  }
}

class _Menu extends StatelessWidget {
  const _Menu(this.icon, this.title, this.sub, this.onTap);
  final IconData icon;
  final String title, sub;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Material(
    color: Colors.white,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(18),
      side: const BorderSide(color: C.line),
    ),
    child: InkWell(
      borderRadius: BorderRadius.circular(18),
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: C.teal, size: 26),
            const SizedBox(height: 10),
            Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700)),
            const SizedBox(height: 2),
            Text(
              sub,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 12, color: C.grey),
            ),
          ],
        ),
      ),
    ),
  );
}
