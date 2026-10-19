import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';

import '../data/materi.dart';
import '../data/progress.dart';
import '../theme.dart';
import '../widgets/common.dart';

/// Rekam & bandingkan. Rekaman hanya disimpan di perangkat dan tidak diunggah.
class PracticeScreen extends StatefulWidget {
  const PracticeScreen({super.key, required this.id});
  final String id;

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  final _rec = AudioRecorder();
  final _player = AudioPlayer();
  final _klip = GlobalKey<KlipGuruState>();
  StreamSubscription<Amplitude>? _ampSub;
  final List<double> _amps = [];
  String? _path;
  bool _merekam = false;
  bool _memutar = false;
  CameraController? _cam;
  String? _camError;
  late List<bool> _cek;

  static const _cekUmum = [
    'Suara keluar dari titik makhraj yang disorot',
    'Bunyinya sama dengan contoh guru',
    'Tidak tertukar dengan huruf yang mirip',
  ];

  @override
  void initState() {
    super.initState();
    final h = context.read<Materi>().hurufById(widget.id);
    _cek = List.filled((h.pelajaran?.latihan?.cek ?? _cekUmum).length, false);
    _player.onPlayerComplete.listen((_) => mounted ? setState(() => _memutar = false) : null);
  }

  @override
  void dispose() {
    _ampSub?.cancel();
    _rec.dispose();
    _player.dispose();
    _cam?.dispose();
    super.dispose();
  }

  void _pesan(String s) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(s)));

  Future<void> _rekam() async {
    if (_merekam) {
      final p = await _rec.stop();
      await _ampSub?.cancel();
      setState(() {
        _merekam = false;
        _path = p;
      });
      return;
    }
    if (!await _rec.hasPermission()) {
      _pesan('Izin mikrofon dibutuhkan untuk merekam.');
      return;
    }
    var target = '';
    if (!kIsWeb) {
      final dir = await getTemporaryDirectory();
      target = '${dir.path}/rekaman_${widget.id}.m4a';
    }
    await _player.stop();
    await _rec.start(RecordConfig(encoder: kIsWeb ? AudioEncoder.opus : AudioEncoder.aacLc), path: target);
    _amps.clear();
    _ampSub = _rec.onAmplitudeChanged(const Duration(milliseconds: 90)).listen((a) {
      if (mounted) setState(() => _amps.add(a.current));
    });
    setState(() {
      _merekam = true;
      _path = null;
    });
  }

  Future<void> _putarRekaman() async {
    final p = _path;
    if (p == null) return;
    if (_memutar) {
      await _player.stop();
      setState(() => _memutar = false);
      return;
    }
    await _player.play(kIsWeb ? UrlSource(p) : DeviceFileSource(p));
    setState(() => _memutar = true);
  }

  Future<void> _cermin() async {
    if (_cam != null) {
      await _cam!.dispose();
      setState(() => _cam = null);
      return;
    }
    try {
      final cams = await availableCameras();
      if (cams.isEmpty) throw CameraException('none', 'Kamera tidak ditemukan');
      final depan = cams.firstWhere((c) => c.lensDirection == CameraLensDirection.front, orElse: () => cams.first);
      final c = CameraController(depan, ResolutionPreset.medium, enableAudio: false);
      await c.initialize();
      setState(() {
        _cam = c;
        _camError = null;
      });
    } catch (e) {
      setState(() => _camError = 'Kamera tidak dapat dibuka. Periksa izin kamera.');
    }
  }

  /// Ringkas amplitudo (dBFS) menjadi 34 batang.
  List<double> _batang() {
    const n = 34;
    if (_amps.isEmpty) return [];
    final out = <double>[];
    for (var i = 0; i < n; i++) {
      final a = _amps[(i * _amps.length / n).floor().clamp(0, _amps.length - 1)];
      out.add(((a + 50) / 50).clamp(0.08, 1.0));
    }
    return out;
  }

  @override
  Widget build(BuildContext context) {
    final materi = context.read<Materi>();
    final prog = context.watch<Progress>();
    final h = materi.hurufById(widget.id);
    final lat = h.pelajaran?.latihan;
    final cekList = lat?.cek ?? _cekUmum;
    final semua = _cek.every((x) => x);

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
          children: [
            const Header('Rekam & bandingkan'),
            const SizedBox(height: 14),
            Center(
              child: Column(
                children: [
                  const Text('Ucapkan', style: TextStyle(fontSize: 13, color: C.grey)),
                  const SizedBox(height: 10),
                  Text(lat?.teks ?? h.huruf, textDirection: TextDirection.rtl, style: arab(52, height: 1.5)),
                  Text(lat?.baca ?? 'huruf ${h.nama}', style: const TextStyle(fontSize: 13, color: C.grey)),
                ],
              ),
            ),
            const SizedBox(height: 14),
            _CerminBox(cam: _cam, error: _camError, onToggle: _cermin),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: kCard,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Contoh: ${materi.guru}',
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: C.teal),
                  ),
                  const SizedBox(height: 8),
                  if (h.video != null) KlipGuru(key: _klip, videoId: h.video!) else const VideoKosong(),
                  const SizedBox(height: 14),
                  Row(
                    children: [
                      IconButton(
                        tooltip: _memutar ? 'Hentikan rekamanmu' : 'Putar rekamanmu',
                        onPressed: _path == null ? null : _putarRekaman,
                        style: IconButton.styleFrom(
                          backgroundColor: C.goldLight,
                          disabledBackgroundColor: C.goldLight.withValues(alpha: 0.5),
                          fixedSize: const Size(44, 44),
                        ),
                        icon: Icon(_memutar ? Icons.stop : Icons.play_arrow, color: C.goldDark),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Rekamanmu',
                              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: C.goldDark),
                            ),
                            const SizedBox(height: 6),
                            SizedBox(
                              height: 32,
                              child: _amps.isEmpty
                                  ? const Align(
                                      alignment: Alignment.centerLeft,
                                      child: Text('Belum ada rekaman', style: TextStyle(fontSize: 13, color: C.grey)),
                                    )
                                  : Row(
                                      children: [
                                        for (final b in _batang()) ...[
                                          Container(
                                            width: 4,
                                            height: 32 * b,
                                            decoration: BoxDecoration(
                                              color: C.goldDeep,
                                              borderRadius: BorderRadius.circular(2),
                                            ),
                                          ),
                                          const SizedBox(width: 3),
                                        ],
                                      ],
                                    ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Putar contoh guru, lalu rekamanmu, secara bergantian.',
                    style: TextStyle(fontSize: 12, color: C.grey),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            BigButton(
              _merekam ? 'Berhenti merekam' : (_path == null ? 'Tekan untuk merekam' : 'Rekam ulang'),
              icon: _merekam ? Icons.stop : Icons.mic_none,
              color: _merekam ? const Color(0xFFB4321F) : C.ink,
              onPressed: _rekam,
            ),
            const SizedBox(height: 14),
            Container(
              padding: const EdgeInsets.fromLTRB(16, 14, 16, 8),
              decoration: kCard,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Cek sendiri bacaanmu', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700)),
                  for (final (i, c) in cekList.indexed)
                    CheckboxListTile(
                      value: _cek[i],
                      onChanged: (v) => setState(() => _cek[i] = v ?? false),
                      title: Text(c, style: const TextStyle(fontSize: 14)),
                      controlAffinity: ListTileControlAffinity.leading,
                      contentPadding: EdgeInsets.zero,
                      activeColor: C.teal,
                      dense: true,
                    ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            BigButton(
              prog.sudah(h.id) ? 'Huruf ${h.nama} sudah dikuasai' : 'Semua sudah benar, tandai dikuasai',
              icon: Icons.check_circle_outline,
              onPressed: semua && !prog.sudah(h.id)
                  ? () {
                      prog.tandai(h.id, true);
                      _pesan('Alhamdulillah, huruf ${h.nama} ditandai dikuasai.');
                    }
                  : null,
            ),
            const SizedBox(height: 10),
            const BigButton('Kirim ke ustaz untuk dikoreksi (Tahap 2)', outline: true, onPressed: null),
          ],
        ),
      ),
    );
  }
}

class _CerminBox extends StatelessWidget {
  const _CerminBox({required this.cam, required this.error, required this.onToggle});
  final CameraController? cam;
  final String? error;
  final VoidCallback onToggle;

  @override
  Widget build(BuildContext context) {
    final c = cam;
    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: Container(
        height: 180,
        color: C.night,
        child: Stack(
          children: [
            if (c != null && c.value.isInitialized)
              Positioned.fill(
                child: FittedBox(
                  fit: BoxFit.cover,
                  child: SizedBox(
                    width: c.value.previewSize?.height ?? 300,
                    height: c.value.previewSize?.width ?? 400,
                    child: CameraPreview(c),
                  ),
                ),
              )
            else
              Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    CustomPaint(size: const Size(150, 90), painter: _BibirPainter()),
                    const SizedBox(height: 8),
                    Text(
                      error ?? 'Nyalakan cermin untuk melihat gerak bibirmu',
                      style: const TextStyle(fontSize: 12, color: Color(0xFFC9CEDA)),
                    ),
                  ],
                ),
              ),
            Positioned(
              left: 12,
              top: 12,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(color: C.ink, borderRadius: BorderRadius.circular(10)),
                child: const Text(
                  'Mode cermin',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.white),
                ),
              ),
            ),
            Positioned(
              right: 8,
              top: 8,
              child: IconButton(
                tooltip: c == null ? 'Nyalakan kamera depan' : 'Matikan kamera',
                onPressed: onToggle,
                style: IconButton.styleFrom(backgroundColor: Colors.white),
                icon: Icon(c == null ? Icons.videocam_outlined : Icons.videocam_off_outlined, color: C.ink),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Garis bantu bentuk bibir.
class _BibirPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size s) {
    final p = Path()
      ..moveTo(10, 45)
      ..cubicTo(40, 18, 60, 22, 75, 30)
      ..cubicTo(90, 22, 110, 18, 140, 45)
      ..cubicTo(110, 72, 40, 72, 10, 45)
      ..close();
    final paint = Paint()
      ..color = C.goldMid
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;
    for (final m in p.computeMetrics()) {
      var d = 0.0;
      while (d < m.length) {
        canvas.drawPath(m.extractPath(d, d + 6), paint);
        d += 11;
      }
    }
  }

  @override
  bool shouldRepaint(_) => false;
}
