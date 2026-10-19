import 'dart:convert';

import 'package:flutter/services.dart';

List<double> _nums(dynamic v) => (v as List).map((e) => (e as num).toDouble()).toList();

class Area {
  Area.fromJson(Map<String, dynamic> j)
    : id = j['id'],
      nama = j['nama'],
      arti = j['arti'],
      deskripsi = j['deskripsi'],
      elips = _nums(j['elips']);
  final String id, nama, arti, deskripsi;

  /// cx, cy, rx, ry dalam koordinat penampang kepala (300 x 240).
  final List<double> elips;
}

class Langkah {
  Langkah.fromJson(Map<String, dynamic> j)
    : label = j['label'],
      judul = j['judul'],
      isi = j['isi'],
      r = (j['r'] as num).toDouble(),
      panah = j['panah'];
  final String label, judul, isi, panah;
  final double r;
}

class Sifat {
  Sifat.fromJson(Map<String, dynamic> j) : nama = j['nama'], arti = j['arti'], tonjol = j['tonjol'] == true;
  final String nama, arti;
  final bool tonjol;
}

class Harakat {
  Harakat.fromJson(Map<String, dynamic> j)
    : teks = j['teks'],
      label = j['label'],
      mulai = (j['mulai'] as num?)?.toDouble(),
      selesai = (j['selesai'] as num?)?.toDouble();
  final String teks, label;

  /// Detik mulai/selesai potongan pada video rujukan; null = belum dicatat.
  final double? mulai, selesai;
}

class Latihan {
  Latihan.fromJson(Map<String, dynamic> j) : teks = j['teks'], baca = j['baca'], cek = List<String>.from(j['cek']);
  final String teks, baca;
  final List<String> cek;
}

class Contoh {
  Contoh.fromJson(Map<String, dynamic> j) : kata = j['kata'], baca = j['baca'], arti = j['arti'];
  final String kata, baca, arti;
}

class Pelajaran {
  Pelajaran.fromJson(Map<String, dynamic> j)
    : makhraj = j['makhraj'],
      langkah = [for (final x in (j['langkah'] ?? [])) Langkah.fromJson(x)],
      sifat = [for (final x in (j['sifat'] ?? [])) Sifat.fromJson(x)],
      kesalahanUmum = j['kesalahanUmum'],
      harakat = [for (final x in (j['harakat'] ?? [])) Harakat.fromJson(x)],
      latihan = j['latihan'] == null ? null : Latihan.fromJson(j['latihan']),
      contoh = j['contoh'] == null ? null : Contoh.fromJson(j['contoh']),
      tervalidasi = j['tervalidasi'] == true;
  final String makhraj;
  final List<Langkah> langkah;
  final List<Sifat> sifat;
  final String? kesalahanUmum;
  final List<Harakat> harakat;
  final Latihan? latihan;
  final Contoh? contoh;
  final bool tervalidasi;

  /// Nama titik makhraj yang ditulis tebal pertama kali, misalnya "wasthul halq".
  String? get namaTitik {
    final m = RegExp(r'\*\*(.+?)\*\*').firstMatch(makhraj);
    return m?.group(1);
  }
}

class Huruf {
  Huruf.fromJson(Map<String, dynamic> j, this.urutan)
    : id = j['id'],
      huruf = j['huruf'],
      nama = j['nama'],
      area = j['area'],
      video = j['video'],
      titik = j['titik'] == null ? null : _nums(j['titik']),
      pelajaran = j['pelajaran'] == null ? null : Pelajaran.fromJson(j['pelajaran']);
  final String id, huruf, nama, area;
  final String? video;

  /// cx, cy, r titik makhraj spesifik (kalau sudah dipetakan).
  final List<double>? titik;
  final Pelajaran? pelajaran;
  final int urutan;
}

class Kuis {
  Kuis.fromJson(Map<String, dynamic> j) : tanya = j['tanya'], jawab = j['jawab'];
  final String tanya, jawab;
}

class Mirip {
  Mirip.fromJson(Map<String, dynamic> j)
    : a = j['a'],
      b = j['b'],
      judul = j['judul'],
      ringkas = j['ringkas'],
      kuis = [for (final x in (j['kuis'] ?? [])) Kuis.fromJson(x)];
  final String a, b;
  final String? judul, ringkas;
  final List<Kuis> kuis;
}

class Materi {
  Materi._(this.area, this.anggotaArea, this.huruf, this.mirip, this.guru, this.kanal);

  final List<Area> area;
  final Map<String, List<String>> anggotaArea;
  final List<Huruf> huruf;
  final List<Mirip> mirip;
  final String guru, kanal;

  static Future<Materi> load() async {
    final j = jsonDecode(await rootBundle.loadString('assets/data/materi.json')) as Map<String, dynamic>;
    final hurufList = <Huruf>[];
    for (final (i, x) in (j['huruf'] as List).indexed) {
      hurufList.add(Huruf.fromJson(x, i + 1));
    }
    return Materi._(
      [for (final x in j['area']) Area.fromJson(x)],
      {for (final e in (j['anggotaArea'] as Map).entries) e.key as String: List<String>.from(e.value)},
      hurufList,
      [for (final x in j['mirip']) Mirip.fromJson(x)],
      j['sumberVideo']['guru'],
      j['sumberVideo']['kanal'],
    );
  }

  Huruf hurufById(String id) => huruf.firstWhere((h) => h.id == id);
  Huruf? hurufOrNull(String id) => huruf.where((h) => h.id == id).firstOrNull;
  Area areaById(String id) => area.firstWhere((a) => a.id == id);

  /// Elips yang disorot untuk sebuah huruf: titik spesifiknya, atau seluruh area.
  List<double> sorotHuruf(Huruf h) {
    final t = h.titik;
    if (t != null) return [t[0], t[1], t[2], t[2]];
    return areaById(h.area).elips;
  }
}
