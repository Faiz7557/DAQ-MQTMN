import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../theme.dart';
import '../widgets/common.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final prog = context.watch<Progress>();
    final tervalidasi = materi.huruf.where((h) => h.pelajaran?.tervalidasi == true).length;
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 28, 20, 24),
      children: [
        const Text('Profil', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
        const SizedBox(height: 14),
        Row(
          children: [
            Expanded(child: _Stat('${prog.dikuasai.length}/${materi.huruf.length}', 'huruf dikuasai')),
            const SizedBox(width: 10),
            Expanded(child: _Stat('${prog.streak}', 'hari beruntun')),
          ],
        ),
        const SizedBox(height: 14),
        const Note(
          Text(
            'Progres disimpan di perangkat ini. Akun dan sinkronisasi antarperangkat akan aktif '
            'setelah proyek Firebase dikonfigurasi.',
          ),
        ),
        const SizedBox(height: 18),
        Container(
          padding: const EdgeInsets.all(18),
          decoration: kCard,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SectionTitle('Sumber dan atribusi'),
              const SizedBox(height: 10),
              _Sumber(
                'Teks Al-Qur\'an',
                'Tanzil Project (tanzil.net), teks Utsmani, lisensi CC BY 3.0. Teks ditampilkan tanpa perubahan.',
              ),
              _Sumber(
                'Terjemahan',
                'Al-Qur\'an dan Terjemahannya, Kementerian Agama RI, melalui Tanzil. Penggunaan nonkomersial.',
              ),
              _Sumber(
                'Contoh pelafalan',
                '${materi.guru}, video kanal YouTube ${materi.kanal}, diputar melalui pemutar resmi YouTube.',
              ),
              _Sumber(
                'Materi makhraj',
                'Disusun dari Al-Muqaddimah al-Jazariyyah dan At-Tajwid al-Mushawwar. $tervalidasi dari ${materi.huruf.length} pelajaran sudah divalidasi pengajar tahsin.',
              ),
            ],
          ),
        ),
        const SizedBox(height: 18),
        BigButton(
          'Atur ulang progres',
          icon: Icons.restart_alt,
          outline: true,
          color: C.grey,
          onPressed: () async {
            final ok = await showDialog<bool>(
              context: context,
              builder: (c) => AlertDialog(
                title: const Text('Atur ulang progres?'),
                content: const Text(
                  'Semua huruf yang ditandai dikuasai dan catatan hari beruntun akan dihapus dari perangkat ini.',
                ),
                actions: [
                  TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('Batal')),
                  FilledButton(onPressed: () => Navigator.pop(c, true), child: const Text('Atur ulang')),
                ],
              ),
            );
            if (ok == true) await prog.reset();
          },
        ),
        const SizedBox(height: 14),
        const Center(
          child: Text('Makhraj MVP 0.1.0', style: TextStyle(fontSize: 12, color: C.grey)),
        ),
      ],
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat(this.value, this.label);
  final String value, label;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: kCard,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          value,
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w700, color: C.teal),
        ),
        Text(label, style: const TextStyle(fontSize: 13, color: C.grey)),
      ],
    ),
  );
}

class _Sumber extends StatelessWidget {
  const _Sumber(this.title, this.body);
  final String title, body;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700)),
        Text(body, style: const TextStyle(fontSize: 13, height: 1.5, color: Color(0xFF3A4152))),
      ],
    ),
  );
}
