import 'dart:convert';

import 'package:flutter/services.dart';

class Surah {
  Surah.fromJson(Map<String, dynamic> j)
    : n = j['n'],
      name = j['name'],
      tname = j['tname'],
      ename = j['ename'],
      type = j['type'],
      basmalah = j['basmalah'] == true,
      ayahs = List<String>.from(j['ayahs']);
  final int n;
  final String name, tname, ename, type;
  final bool basmalah;
  final List<String> ayahs;
}

/// Teks Al-Qur'an Tanzil (Utsmani) dan terjemahan Kemenag. Teks tidak diubah.
class Quran {
  Quran._(this.basmalah, this.suras);

  final String basmalah;
  final List<Surah> suras;
  List<List<String>>? _terjemah;

  static Future<Quran> load() async {
    final j = jsonDecode(await rootBundle.loadString('assets/quran/quran.json')) as Map<String, dynamic>;
    return Quran._(j['basmalah'], [for (final s in j['suras']) Surah.fromJson(s)]);
  }

  Future<List<List<String>>> terjemah() async {
    return _terjemah ??= [
      for (final s in jsonDecode(await rootBundle.loadString('assets/quran/id.json')) as List) List<String>.from(s),
    ];
  }
}

/// Bentuk tulisan yang dihitung sebagai huruf yang sama ketika menyorot kata di mushaf.
const Map<String, String> _varian = {'ا': 'اأإآٱ', 'ء': 'ءأإؤئ', 'ه': 'ه', 'ي': 'يى'};

Set<int> kodeHuruf(String huruf) => (_varian[huruf] ?? huruf).runes.toSet();

/// Apakah kata memuat huruf; harakat dan tanda baca otomatis tidak ikut dicocokkan.
bool kataMemuat(String kata, Set<int> kode) => kata.runes.any(kode.contains);
