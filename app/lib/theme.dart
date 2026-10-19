import 'package:flutter/material.dart';

/// Palet mengikuti purwarupa desain Makhraj.
class C {
  static const teal = Color(0xFF0F5E5E);
  static const tealDark = Color(0xFF0A4444);
  static const tealLight = Color(0xFFDCEDEA);
  static const tealMid = Color(0xFF9CC7C1);
  static const gold = Color(0xFFC8901E);
  static const goldMid = Color(0xFFE2A93B);
  static const goldDeep = Color(0xFFB57F14);
  static const goldDark = Color(0xFF7A520C);
  static const goldInk = Color(0xFF5A3E08);
  static const goldLight = Color(0xFFF6E7C8);
  static const ink = Color(0xFF1C2333);
  static const grey = Color(0xFF5A6070);
  static const line = Color(0xFFE8E1D3);
  static const border = Color(0xFFD9D0BE);
  static const cream = Color(0xFFFBF8F2);
  static const sand = Color(0xFFF4EFE5);
  static const night = Color(0xFF2A3142);
}

ThemeData buildTheme() {
  final base = ThemeData(
    useMaterial3: true,
    fontFamily: 'Jakarta',
    scaffoldBackgroundColor: C.cream,
    colorScheme: ColorScheme.fromSeed(seedColor: C.teal, primary: C.teal, surface: C.cream),
  );
  return base.copyWith(
    textTheme: base.textTheme.apply(bodyColor: C.ink, displayColor: C.ink, fontFamily: 'Jakarta'),
    snackBarTheme: const SnackBarThemeData(behavior: SnackBarBehavior.floating, backgroundColor: C.ink),
  );
}

TextStyle arab(double size, {Color color = C.ink, FontWeight weight = FontWeight.w700, double height = 1.6}) =>
    TextStyle(fontFamily: 'Naskh', fontSize: size, color: color, fontWeight: weight, height: height);

const kCard = BoxDecoration(
  color: Colors.white,
  borderRadius: BorderRadius.all(Radius.circular(20)),
  border: Border.fromBorderSide(BorderSide(color: C.line)),
);

/// Teks dengan penanda **tebal** sederhana.
Text richText(String s, {TextStyle? style}) {
  final base = style ?? const TextStyle(fontSize: 14, height: 1.6, color: Color(0xFF3A4152));
  final spans = <TextSpan>[];
  final parts = s.split('**');
  for (var i = 0; i < parts.length; i++) {
    spans.add(
      TextSpan(
        text: parts[i],
        style: i.isOdd ? const TextStyle(fontWeight: FontWeight.w700) : null,
      ),
    );
  }
  return Text.rich(TextSpan(style: base, children: spans));
}

String angkaArab(int n) {
  const d = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return n.toString().split('').map((c) => d[int.parse(c)]).join();
}
