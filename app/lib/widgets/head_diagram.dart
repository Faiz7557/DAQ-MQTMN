import 'package:flutter/material.dart';

import '../theme.dart';

/// Penampang samping kepala (koordinat 300 x 240), sama dengan purwarupa desain.
/// Ilustrasi sederhana; perlu diganti gambar anatomi yang dicek guru tahsin.
const _outline =
    'M262 14 C190 8 128 30 112 70 C106 86 100 98 80 116 L94 124 C92 130 86 136 82 140 C86 144 90 146 90 147 '
    'C88 149 84 151 82 155 C88 160 92 166 94 172 C96 182 104 190 130 194 C150 197 160 202 165 212 L170 236 '
    'L292 236 L292 14 Z';
const _garis = [
  'M100 114 C140 100 190 98 222 110',
  'M104 124 C150 116 190 118 222 124',
  'M92 136 C130 126 185 124 214 134 C222 140 224 150 220 160',
  'M222 124 C232 160 232 200 226 236',
  'M204 196 C202 212 200 225 198 236',
];
const _lidah = 'M92 150 C112 138 165 132 196 144 C210 152 212 172 204 196 L182 196 C160 180 120 168 92 156 Z';

const kViewPenuh = Rect.fromLTWH(0, 0, 300, 240);
const kViewTenggorokan = Rect.fromLTWH(120, 90, 140, 150);

/// Parser kecil untuk path SVG absolut (M, L, C, Z).
Path parsePath(String d) {
  final t = RegExp(r'[MLCZ]|-?\d*\.?\d+').allMatches(d).map((m) => m.group(0)!).toList();
  final p = Path();
  var i = 0;
  String cmd = 'M';
  double n() => double.parse(t[i++]);
  while (i < t.length) {
    if (RegExp(r'[MLCZ]').hasMatch(t[i])) cmd = t[i++];
    switch (cmd) {
      case 'M':
        p.moveTo(n(), n());
        cmd = 'L';
      case 'L':
        p.lineTo(n(), n());
      case 'C':
        p.cubicTo(n(), n(), n(), n(), n(), n());
      case 'Z':
        p.close();
    }
  }
  return p;
}

final _pOutline = parsePath(_outline);
final _pGaris = [for (final g in _garis) parsePath(g)];
final _pLidah = parsePath(_lidah);

class _HeadPainter extends CustomPainter {
  _HeadPainter(this.sorot, this.panah, this.view);

  final Rect? sorot;
  final String? panah;
  final Rect view;

  @override
  void paint(Canvas canvas, Size size) {
    final s = size.width / view.width;
    canvas.save();
    canvas.clipRRect(RRect.fromRectAndRadius(Offset.zero & size, const Radius.circular(16)));
    canvas.scale(s);
    canvas.translate(-view.left, -view.top);
    canvas.drawRect(view, Paint()..color = C.sand);
    canvas.drawPath(_pOutline, Paint()..color = Colors.white);
    canvas.drawPath(
      _pOutline,
      Paint()
        ..color = C.ink
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2
        ..strokeJoin = StrokeJoin.round,
    );
    final g = Paint()
      ..color = const Color(0xFF9AA0AE)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2
      ..strokeCap = StrokeCap.round;
    for (final p in _pGaris) {
      canvas.drawPath(p, g);
    }
    canvas.drawPath(_pLidah, Paint()..color = const Color(0xFFF2CFC6));
    canvas.drawPath(
      _pLidah,
      Paint()
        ..color = const Color(0xFFC98B80)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5,
    );
    final r = sorot;
    if (r != null) {
      canvas.drawOval(r, Paint()..color = C.goldMid.withValues(alpha: 0.45));
      canvas.drawOval(
        r,
        Paint()
          ..color = C.goldDeep
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2.5,
      );
    }
    if (panah != null) {
      canvas.drawPath(
        parsePath(panah!),
        Paint()
          ..color = C.teal
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2.5
          ..strokeCap = StrokeCap.round
          ..strokeJoin = StrokeJoin.round,
      );
    }
    canvas.restore();
  }

  @override
  bool shouldRepaint(_HeadPainter old) => old.sorot != sorot || old.panah != panah || old.view != view;
}

/// Penampang kepala dengan sorotan beranimasi.
/// [sorot] = cx, cy, rx, ry. [onTap] menerima titik dalam koordinat penampang.
class HeadDiagram extends StatelessWidget {
  const HeadDiagram({super.key, this.sorot, this.panah, this.view = kViewPenuh, this.onTap, this.label});

  final List<double>? sorot;
  final String? panah;
  final Rect view;
  final void Function(Offset titik)? onTap;
  final String? label;

  @override
  Widget build(BuildContext context) {
    final target = sorot == null
        ? null
        : Rect.fromCenter(center: Offset(sorot![0], sorot![1]), width: sorot![2] * 2, height: sorot![3] * 2);
    return Semantics(
      label: label ?? 'Penampang samping mulut dan tenggorokan',
      image: true,
      child: AspectRatio(
        aspectRatio: view.width / view.height,
        child: LayoutBuilder(
          builder: (context, c) {
            final s = c.maxWidth / view.width;
            return GestureDetector(
              onTapUp: onTap == null
                  ? null
                  : (d) => onTap!(Offset(d.localPosition.dx / s + view.left, d.localPosition.dy / s + view.top)),
              child: TweenAnimationBuilder<Rect?>(
                tween: RectTween(end: target),
                duration: const Duration(milliseconds: 320),
                curve: Curves.easeOutCubic,
                builder: (context, r, _) => CustomPaint(painter: _HeadPainter(r, panah, view), size: Size.infinite),
              ),
            );
          },
        ),
      ),
    );
  }
}
