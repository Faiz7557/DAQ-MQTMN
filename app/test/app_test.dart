import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:makhraj/data/materi.dart';
import 'package:makhraj/data/progress.dart';
import 'package:makhraj/data/quran.dart';
import 'package:makhraj/main.dart';
import 'package:makhraj/widgets/head_diagram.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<(Materi, Quran, Progress)> _load() async {
  SharedPreferences.setMockInitialValues({});
  final materi = await Materi.load();
  final quran = await Quran.load();
  final progress = Progress();
  await progress.init();
  return (materi, quran, progress);
}

Future<Progress> _pump(WidgetTester tester) async {
  tester.view.physicalSize = const Size(390 * 3, 844 * 3);
  tester.view.devicePixelRatio = 3;
  addTearDown(tester.view.reset);
  final (materi, quran, progress) = (await tester.runAsync(_load))!;
  await tester.pumpWidget(MakhrajApp(materi: materi, quran: quran, progress: progress));
  await tester.pumpAndSettle();
  return progress;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('data', () {
    test('materi memuat 29 huruf dan setiap anggota area valid', () async {
      final m = await Materi.load();
      expect(m.huruf.length, 29);
      expect(m.area.length, 5);
      for (final ids in m.anggotaArea.values) {
        for (final id in ids) {
          expect(m.hurufOrNull(id), isNotNull, reason: id);
        }
      }
      for (final p in m.mirip) {
        expect(m.hurufOrNull(p.a), isNotNull);
        expect(m.hurufOrNull(p.b), isNotNull);
        for (final k in p.kuis) {
          expect([p.a, p.b], contains(k.jawab));
        }
      }
      expect(m.hurufById('ba').pelajaran!.langkah.length, 3);
    });

    test('teks Tanzil lengkap dan basmalah dipisah', () async {
      final q = await Quran.load();
      expect(q.suras.length, 114);
      expect(q.suras.fold<int>(0, (n, s) => n + s.ayahs.length), 6236);
      expect(q.suras[0].basmalah, isFalse); // Al-Fatihah: basmalah adalah ayat 1
      expect(q.suras[1].basmalah, isTrue);
      expect(q.suras[8].basmalah, isFalse); // At-Taubah
      expect(q.suras[1].ayahs.first.startsWith('بِسْمِ'), isFalse);
      final t = await q.terjemah();
      expect(t[0].length, 7);
    });

    test('sorot huruf ba di Al-Fatihah menandai 4 kata', () async {
      final q = await Quran.load();
      final kode = kodeHuruf('ب');
      final n = q.suras[0].ayahs.expand((a) => a.split(' ')).where((w) => kataMemuat(w, kode)).length;
      expect(n, 4);
    });

    test('parser path SVG menghasilkan bentuk tertutup', () {
      final p = parsePath('M0 0 L10 0 C10 5 5 10 0 10 Z');
      expect(p.getBounds().width, closeTo(10, 0.01));
    });
  });

  group('alur aplikasi', () {
    testWidgets('beranda menampilkan pelajaran berikutnya dan membuka pelajaran', (tester) async {
      await _pump(tester);
      expect(find.text('Yuk lanjut belajar'), findsOneWidget);
      expect(find.text('0 / 29'), findsOneWidget);
      await tester.tap(find.text('Mulai belajar'));
      await tester.pumpAndSettle();
      expect(find.text('Huruf Alif'), findsOneWidget);
      expect(find.textContaining('belum tersedia'), findsOneWidget);
    });

    testWidgets('pelajaran ba: langkah animasi bisa dipilih dan huruf bisa ditandai', (tester) async {
      final prog = await _pump(tester);
      final router = tester.widget<MaterialApp>(find.byType(MaterialApp)).routerConfig!;
      (router as dynamic).go('/huruf/ba');
      await tester.pumpAndSettle();
      expect(find.text('Rapatkan kedua bibir'), findsOneWidget);
      await tester.tap(find.text('3 · Lepaskan'));
      await tester.pumpAndSettle();
      expect(find.text('Lepaskan dengan cepat'), findsOneWidget);
      final tandai = find.text('Tandai sudah dikuasai');
      await tester.scrollUntilVisible(tandai, 300, scrollable: find.byType(Scrollable).first);
      await tester.tap(tandai);
      await tester.pumpAndSettle();
      expect(prog.sudah('ba'), isTrue);
    });

    testWidgets('peta: memilih area Al-Halq menampilkan 6 huruf', (tester) async {
      await _pump(tester);
      await tester.tap(find.text('Tahsin'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Al-Halq'));
      await tester.pumpAndSettle();
      expect(find.text('6 huruf · ketuk untuk belajar'), findsOneWidget);
    });

    testWidgets('kuis huruf mirip memberi umpan balik', (tester) async {
      await _pump(tester);
      final router = tester.widget<MaterialApp>(find.byType(MaterialApp)).routerConfig!;
      (router as dynamic).go('/mirip/0');
      await tester.pumpAndSettle();
      // Tombol jawaban adalah teks ح terakhir (yang pertama ada di kartu perbandingan).
      final jawab = find.text('ح').last;
      await tester.ensureVisible(jawab);
      await tester.pumpAndSettle();
      await tester.tap(jawab);
      await tester.pumpAndSettle();
      expect(find.textContaining('Benar!'), findsOneWidget);
    });

    testWidgets('mushaf: sorotan bisa dimatikan', (tester) async {
      await _pump(tester);
      final router = tester.widget<MaterialApp>(find.byType(MaterialApp)).routerConfig!;
      (router as dynamic).go('/mushaf/1?huruf=ba');
      await tester.pumpAndSettle();
      expect(find.text('4 kata dengan huruf ب di surah ini'), findsOneWidget);
      await tester.tap(find.byType(Switch));
      await tester.pumpAndSettle();
      expect(find.text('Sorotan dimatikan'), findsOneWidget);
    });
  });
}
