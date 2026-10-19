import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../theme.dart';
import '../widgets/common.dart';
import '../widgets/head_diagram.dart';

class PetaScreen extends StatefulWidget {
  const PetaScreen({super.key, this.areaAwal});
  final String? areaAwal;

  @override
  State<PetaScreen> createState() => _PetaScreenState();
}

class _PetaScreenState extends State<PetaScreen> {
  late String _area = widget.areaAwal ?? 'syafatain';

  /// Ketukan pada penampang memilih area terkecil yang memuat titik ketukan.
  void _tap(Offset p, List<Area> areas) {
    Area? best;
    for (final a in areas) {
      final e = a.elips;
      final dx = (p.dx - e[0]) / (e[2] + 6), dy = (p.dy - e[1]) / (e[3] + 6);
      if (dx * dx + dy * dy <= 1 && (best == null || e[2] * e[3] < best.elips[2] * best.elips[3])) best = a;
    }
    if (best != null) setState(() => _area = best!.id);
  }

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final prog = context.watch<Progress>();
    final area = materi.areaById(_area);
    final anggota = [for (final id in materi.anggotaArea[_area]!) materi.hurufById(id)];

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
      children: [
        const SizedBox(
          height: 44,
          child: Align(
            alignment: Alignment.centerLeft,
            child: Text('Peta Makhraj', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
          ),
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: kCard.copyWith(borderRadius: BorderRadius.circular(24)),
          child: Column(
            children: [
              HeadDiagram(
                sorot: area.elips,
                onTap: (p) => _tap(p, materi.area),
                label: 'Penampang samping kepala, menyorot ${area.nama} (${area.arti})',
              ),
              const SizedBox(height: 6),
              const Text(
                'Penampang samping kepala · ketuk area untuk melihat hurufnya',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 12, color: C.grey),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (final a in materi.area)
              ChoiceChip(
                label: Text(a.nama),
                selected: a.id == _area,
                showCheckmark: false,
                onSelected: (_) => setState(() => _area = a.id),
                selectedColor: C.teal,
                backgroundColor: Colors.white,
                side: BorderSide(color: a.id == _area ? C.teal : C.border),
                labelStyle: TextStyle(
                  fontFamily: 'Jakarta',
                  fontSize: 13,
                  fontWeight: a.id == _area ? FontWeight.w700 : FontWeight.w600,
                  color: a.id == _area ? Colors.white : C.ink,
                ),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
              ),
          ],
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(18),
          decoration: kCard,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: area.nama,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                    ),
                    TextSpan(
                      text: ' · ${area.arti}',
                      style: const TextStyle(fontSize: 18, color: C.grey),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 4),
              Text(area.deskripsi, style: const TextStyle(fontSize: 14, height: 1.55, color: Color(0xFF3A4152))),
              const SizedBox(height: 12),
              if (anggota.isEmpty)
                const Text(
                  'Ghunnah dibahas pada materi tajwid lanjutan (Tahap 3).',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: C.grey),
                )
              else ...[
                Text(
                  '${anggota.length} huruf · ketuk untuk belajar',
                  style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: C.grey),
                ),
                const SizedBox(height: 10),
                Directionality(
                  textDirection: TextDirection.rtl,
                  child: GridView.count(
                    crossAxisCount: 6,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    mainAxisSpacing: 8,
                    crossAxisSpacing: 8,
                    childAspectRatio: 0.95,
                    children: [
                      for (final h in anggota)
                        LetterTile(
                          h.huruf,
                          size: 48,
                          filled: prog.sudah(h.id),
                          label: 'Belajar huruf ${h.nama}',
                          onTap: () => context.push('/huruf/${h.id}'),
                        ),
                    ],
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }
}
