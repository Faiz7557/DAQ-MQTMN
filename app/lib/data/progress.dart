import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Progres belajar disimpan di perangkat (mode lokal).
/// Sinkronisasi Firestore menyusul setelah proyek Firebase tim dikonfigurasi.
class Progress extends ChangeNotifier {
  SharedPreferences? _p;
  Set<String> dikuasai = {};
  List<String> hariAktif = [];
  int terakhirSurah = 1;

  static String _hari(DateTime d) =>
      '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

  Future<void> init({bool demo = false}) async {
    _p = await SharedPreferences.getInstance();
    if (demo) {
      // Data contoh untuk demo dan tangkapan layar: 3 huruf dikuasai, 5 hari beruntun.
      dikuasai = {'alif', 'mim', 'fa'};
      final now = DateTime.now();
      hariAktif = [for (var i = 4; i >= 0; i--) _hari(now.subtract(Duration(days: i)))];
      terakhirSurah = 1;
      return;
    }
    dikuasai = (_p!.getStringList('dikuasai') ?? []).toSet();
    hariAktif = _p!.getStringList('hariAktif') ?? [];
    terakhirSurah = _p!.getInt('terakhirSurah') ?? 1;
    catatAktif();
  }

  void _simpan() {
    _p?.setStringList('dikuasai', dikuasai.toList());
    _p?.setStringList('hariAktif', hariAktif);
    _p?.setInt('terakhirSurah', terakhirSurah);
  }

  void catatAktif() {
    final today = _hari(DateTime.now());
    if (!hariAktif.contains(today)) {
      hariAktif.add(today);
      if (hariAktif.length > 400) hariAktif.removeAt(0);
      _simpan();
      notifyListeners();
    }
  }

  int get streak {
    final set = hariAktif.toSet();
    var d = DateTime.now();
    var n = 0;
    while (set.contains(_hari(d))) {
      n++;
      d = d.subtract(const Duration(days: 1));
    }
    return n;
  }

  bool sudah(String id) => dikuasai.contains(id);

  void tandai(String id, bool v) {
    v ? dikuasai.add(id) : dikuasai.remove(id);
    catatAktif();
    _simpan();
    notifyListeners();
  }

  void bacaSurah(int n) {
    terakhirSurah = n;
    _simpan();
    notifyListeners();
  }

  Future<void> reset() async {
    dikuasai = {};
    hariAktif = [];
    terakhirSurah = 1;
    await _p?.clear();
    catatAktif();
    notifyListeners();
  }
}
