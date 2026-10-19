import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../theme.dart';
import '../widgets/common.dart';
import '../widgets/head_diagram.dart';

class LessonScreen extends StatefulWidget {
  const LessonScreen({super.key, required this.id});
  final String id;

  @override
  State<LessonScreen> createState() => _LessonScreenState();
}

class _LessonScreenState extends State<LessonScreen> {
  int _step = 0;
  final _klip = GlobalKey<KlipGuruState>();

  void _dengar(Harakat h) {
    _klip.currentState?.putar(mulai: h.mulai);
    if (h.mulai == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Penanda detik untuk harakat ini belum dicatat, jadi video diputar dari awal.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final prog = context.watch<Progress>();
    final h = materi.hurufById(widget.id);
    final area = materi.areaById(h.area);
    final p = h.pelajaran;
    final steps = p?.langkah ?? const <Langkah>[];
    final step = steps.isEmpty ? null : steps[_step];
    final sorot = materi.sorotHuruf(h);
    final sudah = prog.sudah(h.id);

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 32),
          children: [
            Header('Pelajaran ${h.urutan} dari ${materi.huruf.length}', center: true),
            const SizedBox(height: 16),
            Row(
              children: [
                Container(
                  width: 96,
                  height: 96,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: C.teal, borderRadius: BorderRadius.circular(24)),
                  child: Text(h.huruf, style: arab(60, color: Colors.white, height: 1.2)),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Huruf ${h.nama}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w700)),
                      const SizedBox(height: 2),
                      Text(
                        'Area: ${area.nama} (${area.arti.toLowerCase()})',
                        style: const TextStyle(fontSize: 14, color: C.grey),
                      ),
                      const SizedBox(height: 6),
                      if (p != null) ValidasiBadge(tervalidasi: p.tervalidasi),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: kCard.copyWith(borderRadius: BorderRadius.circular(24)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Padding(padding: EdgeInsets.fromLTRB(4, 0, 4, 10), child: SectionTitle('Visualisasi makhraj')),
                  HeadDiagram(
                    sorot: step == null ? sorot : [sorot[0], sorot[1], step.r, step.r],
                    panah: step?.panah,
                    label: 'Penampang samping mulut, menyorot makhraj huruf ${h.nama}',
                  ),
                  if (step != null) ...[
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        for (final (i, s) in steps.indexed) ...[
                          if (i > 0) const SizedBox(width: 8),
                          Expanded(
                            child: _StepButton(s.label, selected: i == _step, onTap: () => setState(() => _step = i)),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 12),
                    Container(
                      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
                      decoration: BoxDecoration(color: C.tealLight, borderRadius: BorderRadius.circular(14)),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            step.judul,
                            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: C.tealDark),
                          ),
                          const SizedBox(height: 4),
                          Text(step.isi, style: const TextStyle(fontSize: 13, height: 1.55, color: Color(0xFF24414A))),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 18),
            const SectionTitle('Dengarkan dari guru'),
            const SizedBox(height: 10),
            if (h.video != null) KlipGuru(key: _klip, videoId: h.video!) else const VideoKosong(),
            const SizedBox(height: 8),
            Text(
              'Latihan Pengucapan Huruf ${h.nama.split(' ').first}',
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
            ),
            Text('${materi.guru} · kanal ${materi.kanal}', style: const TextStyle(fontSize: 13, color: C.grey)),
            if (p != null && p.harakat.isNotEmpty) ...[
              const SizedBox(height: 10),
              Directionality(
                textDirection: TextDirection.rtl,
                child: Row(
                  children: [
                    for (final (i, hk) in p.harakat.indexed) ...[
                      if (i > 0) const SizedBox(width: 8),
                      Expanded(
                        child: Tooltip(
                          message: 'Dengar ${hk.label}',
                          child: OutlinedButton(
                            onPressed: h.video == null ? null : () => _dengar(hk),
                            style: OutlinedButton.styleFrom(
                              minimumSize: const Size(0, 52),
                              side: const BorderSide(color: C.border),
                              backgroundColor: Colors.white,
                              foregroundColor: C.ink,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                            ),
                            child: Text(hk.teks, style: arab(24, weight: FontWeight.w400, height: 1.3)),
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ],
            const SizedBox(height: 18),
            Container(
              padding: const EdgeInsets.all(18),
              decoration: kCard,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SectionTitle('Letak makhraj'),
                  const SizedBox(height: 10),
                  if (p != null)
                    richText(p.makhraj)
                  else
                    Text(area.deskripsi, style: const TextStyle(fontSize: 14, height: 1.6)),
                  if (p?.contoh != null) ...[
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Text(p!.contoh!.kata, style: arab(26, weight: FontWeight.w400)),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            '${p.contoh!.baca} · ${p.contoh!.arti}',
                            style: const TextStyle(fontSize: 13, color: C.grey),
                          ),
                        ),
                      ],
                    ),
                  ],
                  if (p?.kesalahanUmum != null) ...[
                    const SizedBox(height: 12),
                    Note(
                      Text.rich(
                        TextSpan(
                          children: [
                            const TextSpan(
                              text: 'Kesalahan umum: ',
                              style: TextStyle(fontWeight: FontWeight.w700),
                            ),
                            TextSpan(text: p!.kesalahanUmum),
                          ],
                        ),
                      ),
                    ),
                  ],
                  if (p != null && p.sifat.isNotEmpty) ...[
                    const SizedBox(height: 14),
                    const Text(
                      'Sifat huruf',
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: C.grey),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [for (final s in p.sifat) Chip2('${s.nama} · ${s.arti}', gold: s.tonjol)],
                    ),
                  ],
                  if (p == null) ...[
                    const SizedBox(height: 12),
                    const Note(
                      Text(
                        'Materi rinci huruf ini (titik makhraj, sifat, dan kesalahan umum) sedang disusun '
                        'dan akan divalidasi pengajar tahsin bersanad.',
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 18),
            BigButton('Coba ucapkan sendiri', icon: Icons.mic_none, onPressed: () => context.push('/latihan/${h.id}')),
            const SizedBox(height: 10),
            BigButton(
              sudah ? 'Sudah dikuasai · ketuk untuk membatalkan' : 'Tandai sudah dikuasai',
              icon: sudah ? Icons.check_circle : Icons.check_circle_outline,
              outline: true,
              onPressed: () => prog.tandai(h.id, !sudah),
            ),
            const SizedBox(height: 10),
            TextButton.icon(
              onPressed: () => context.push('/mushaf/1?huruf=${h.id}'),
              icon: const Icon(Icons.menu_book_outlined, size: 18),
              label: Text('Cari huruf ${h.huruf} di Al-Fatihah'),
            ),
          ],
        ),
      ),
    );
  }
}

class _StepButton extends StatelessWidget {
  const _StepButton(this.label, {required this.selected, required this.onTap});
  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    selected: selected,
    button: true,
    child: Material(
      color: selected ? C.teal : Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: selected ? C.teal : C.border),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: SizedBox(
          height: 44,
          child: Center(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 12,
                fontWeight: selected ? FontWeight.w700 : FontWeight.w600,
                color: selected ? Colors.white : C.ink,
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
