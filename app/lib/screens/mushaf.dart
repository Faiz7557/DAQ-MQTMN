import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../data/quran.dart';
import '../theme.dart';

/// Daftar surah.
class MushafListScreen extends StatefulWidget {
  const MushafListScreen({super.key});

  @override
  State<MushafListScreen> createState() => _MushafListScreenState();
}

class _MushafListScreenState extends State<MushafListScreen> {
  String _q = '';

  @override
  Widget build(BuildContext context) {
    final quran = context.read<Quran>();
    final prog = context.watch<Progress>();
    final last = quran.suras[prog.terakhirSurah - 1];
    final q = _q.toLowerCase().replaceAll('-', '').replaceAll("'", '');
    final list = quran.suras.where((s) {
      if (q.isEmpty) return true;
      final name = s.tname.toLowerCase().replaceAll('-', '').replaceAll("'", '');
      return name.contains(q) || '${s.n}' == q;
    }).toList();
    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(20, 24, 20, 24),
      itemCount: list.length + 1,
      itemBuilder: (context, i) {
        if (i == 0) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Mushaf', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
              const SizedBox(height: 14),
              TextField(
                decoration: InputDecoration(
                  hintText: 'Cari nama atau nomor surah',
                  prefixIcon: const Icon(Icons.search),
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(16),
                    borderSide: const BorderSide(color: C.line),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(16),
                    borderSide: const BorderSide(color: C.line),
                  ),
                ),
                onChanged: (v) => setState(() => _q = v.trim()),
              ),
              const SizedBox(height: 14),
              Material(
                color: C.teal,
                borderRadius: BorderRadius.circular(20),
                child: InkWell(
                  borderRadius: BorderRadius.circular(20),
                  onTap: () => context.push('/mushaf/${last.n}'),
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Row(
                      children: [
                        const Icon(Icons.bookmark_outline, color: Colors.white),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Terakhir dibaca', style: TextStyle(fontSize: 12, color: Color(0xFFCDE5E1))),
                              Text(
                                last.tname,
                                style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: Colors.white),
                              ),
                            ],
                          ),
                        ),
                        Text(last.name, style: arab(24, color: Colors.white)),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 10),
            ],
          );
        }
        final s = list[i - 1];
        return InkWell(
          onTap: () => context.push('/mushaf/${s.n}'),
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 12),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: C.line)),
            ),
            child: Row(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: C.tealLight, borderRadius: BorderRadius.circular(10)),
                  child: Text(
                    '${s.n}',
                    style: const TextStyle(fontWeight: FontWeight.w700, color: C.teal),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(s.tname, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700)),
                      Text(
                        '${s.type == 'Meccan' ? 'Makkiyah' : 'Madaniyah'} · ${s.ayahs.length} ayat',
                        style: const TextStyle(fontSize: 12, color: C.grey),
                      ),
                    ],
                  ),
                ),
                Text(s.name, style: arab(22, color: C.teal)),
              ],
            ),
          ),
        );
      },
    );
  }
}

/// Pembaca surah dengan sorot huruf yang sudah dipelajari.
class MushafReaderScreen extends StatefulWidget {
  const MushafReaderScreen({super.key, required this.n, this.hurufAwal});
  final int n;
  final String? hurufAwal;

  @override
  State<MushafReaderScreen> createState() => _MushafReaderScreenState();
}

class _MushafReaderScreenState extends State<MushafReaderScreen> {
  bool _sorot = true;
  bool _terjemah = false;
  List<List<String>>? _id;
  late String _hurufId;

  @override
  void initState() {
    super.initState();
    final prog = context.read<Progress>();
    _hurufId = widget.hurufAwal ?? 'ba';
    WidgetsBinding.instance.addPostFrameCallback((_) => prog.bacaSurah(widget.n));
  }

  Future<void> _toggleTerjemah() async {
    if (!_terjemah && _id == null) {
      _id = await context.read<Quran>().terjemah();
    }
    setState(() => _terjemah = !_terjemah);
  }

  @override
  Widget build(BuildContext context) {
    final quran = context.read<Quran>();
    final materi = context.read<Materi>();
    final prog = context.watch<Progress>();
    final s = quran.suras[widget.n - 1];
    final h = materi.hurufById(_hurufId);
    final kode = kodeHuruf(h.huruf);
    var jumlah = 0;
    for (final a in s.ayahs) {
      jumlah += a.split(' ').where((w) => kataMemuat(w, kode)).length;
    }
    final pilihan = <Huruf>{
      h,
      for (final x in materi.huruf)
        if (prog.sudah(x.id)) x,
    }.toList()..sort((a, b) => a.urutan.compareTo(b.urutan));

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(s.tname, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
                        Text(
                          'Surah ke-${s.n} · ${s.ayahs.length} ayat',
                          style: const TextStyle(fontSize: 12, color: C.grey),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    tooltip: _terjemah ? 'Sembunyikan terjemahan' : 'Tampilkan terjemahan',
                    onPressed: _toggleTerjemah,
                    style: IconButton.styleFrom(backgroundColor: _terjemah ? C.teal : C.tealLight),
                    icon: Icon(Icons.translate, color: _terjemah ? Colors.white : C.teal),
                  ),
                  const SizedBox(width: 6),
                  IconButton(
                    tooltip: 'Tutup',
                    onPressed: () => context.canPop() ? context.pop() : context.go('/mushaf'),
                    style: IconButton.styleFrom(backgroundColor: C.tealLight),
                    icon: const Icon(Icons.close, color: C.teal),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Container(
                padding: const EdgeInsets.fromLTRB(12, 10, 10, 10),
                decoration: kCard.copyWith(borderRadius: BorderRadius.circular(16)),
                child: Row(
                  children: [
                    PopupMenuButton<String>(
                      tooltip: 'Pilih huruf yang disorot',
                      onSelected: (id) => setState(() => _hurufId = id),
                      itemBuilder: (_) => [
                        for (final x in pilihan)
                          PopupMenuItem(
                            value: x.id,
                            child: Text('${x.huruf}   ${x.nama}', style: const TextStyle(fontSize: 15)),
                          ),
                      ],
                      child: Container(
                        width: 40,
                        height: 40,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(color: C.goldLight, borderRadius: BorderRadius.circular(10)),
                        child: Text(h.huruf, style: arab(22, color: C.goldDark, height: 1.2)),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Sorot huruf yang dipelajari',
                            style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
                          ),
                          Text(
                            _sorot ? '$jumlah kata dengan huruf ${h.huruf} di surah ini' : 'Sorotan dimatikan',
                            style: const TextStyle(fontSize: 12, color: C.grey),
                          ),
                        ],
                      ),
                    ),
                    Switch(value: _sorot, activeTrackColor: C.teal, onChanged: (v) => setState(() => _sorot = v)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
                itemCount: s.ayahs.length + 2,
                itemBuilder: (context, i) {
                  if (i == 0) {
                    return s.basmalah
                        ? Padding(
                            padding: const EdgeInsets.only(bottom: 8),
                            child: Text(
                              quran.basmalah,
                              textAlign: TextAlign.center,
                              style: arab(22, weight: FontWeight.w400),
                            ),
                          )
                        : const SizedBox.shrink();
                  }
                  if (i == s.ayahs.length + 1) {
                    return const Padding(
                      padding: EdgeInsets.only(top: 16),
                      child: Text(
                        'Teks: Tanzil Project (tanzil.net), CC BY 3.0. Terjemahan: Kementerian Agama RI.',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 11, color: C.grey),
                      ),
                    );
                  }
                  final ayah = s.ayahs[i - 1];
                  return _Ayat(
                    teks: ayah,
                    nomor: i,
                    kode: _sorot ? kode : null,
                    terjemah: _terjemah ? (_id?[s.n - 1][i - 1]) : null,
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Ayat extends StatelessWidget {
  const _Ayat({required this.teks, required this.nomor, this.kode, this.terjemah});
  final String teks;
  final int nomor;
  final Set<int>? kode;
  final String? terjemah;

  @override
  Widget build(BuildContext context) {
    final words = teks.split(' ');
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: C.line)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Directionality(
            textDirection: TextDirection.rtl,
            child: Wrap(
              spacing: 6,
              runSpacing: 4,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                for (final w in words)
                  if (kode != null && kataMemuat(w, kode!))
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6),
                      decoration: BoxDecoration(
                        color: C.goldLight,
                        borderRadius: BorderRadius.circular(8),
                        border: const Border(bottom: BorderSide(color: C.goldMid, width: 3)),
                      ),
                      child: Text(
                        w,
                        style: arab(23, color: C.goldInk, weight: FontWeight.w400, height: 1.9),
                      ),
                    )
                  else
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 2),
                      child: Text(w, style: arab(23, weight: FontWeight.w400, height: 1.9)),
                    ),
                Text(
                  '﴿${angkaArab(nomor)}﴾',
                  style: arab(18, color: C.teal, weight: FontWeight.w400),
                ),
              ],
            ),
          ),
          if (terjemah != null)
            Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Text(
                '$nomor. $terjemah',
                style: const TextStyle(fontSize: 13, height: 1.5, color: Color(0xFF3A4152)),
              ),
            ),
        ],
      ),
    );
  }
}
