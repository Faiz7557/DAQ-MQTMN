import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:youtube_player_iframe/youtube_player_iframe.dart';

import '../theme.dart';

/// Baris judul dengan tombol kembali bulat, seperti purwarupa.
class Header extends StatelessWidget {
  const Header(this.title, {super.key, this.center = false, this.trailing});

  final String title;
  final bool center;
  final Widget? trailing;

  @override
  Widget build(BuildContext context) {
    final back = SizedBox(
      width: 44,
      height: 44,
      child: Material(
        color: Colors.white,
        shape: const CircleBorder(side: BorderSide(color: C.line)),
        child: IconButton(
          tooltip: 'Kembali',
          icon: const Icon(Icons.chevron_left, color: C.ink),
          onPressed: () => context.canPop() ? context.pop() : context.go('/'),
        ),
      ),
    );
    final t = Text(
      title,
      style: TextStyle(
        fontSize: center ? 14 : 17,
        fontWeight: center ? FontWeight.w600 : FontWeight.w700,
        color: center ? C.grey : C.ink,
      ),
    );
    return SizedBox(
      height: 44,
      child: center
          ? Row(
              children: [
                back,
                Expanded(child: Center(child: t)),
                SizedBox(width: 44, child: trailing),
              ],
            )
          : Row(
              children: [
                back,
                const SizedBox(width: 12),
                Expanded(child: t),
                ?trailing,
              ],
            ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  const SectionTitle(this.text, {super.key});
  final String text;

  @override
  Widget build(BuildContext context) => Text(text, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700));
}

/// Kotak huruf hijaiyah kecil.
class LetterTile extends StatelessWidget {
  const LetterTile(
    this.char, {
    super.key,
    this.size = 36,
    this.filled = false,
    this.dashed = false,
    this.onTap,
    this.label,
  });

  final String char;
  final double size;
  final bool filled, dashed;
  final VoidCallback? onTap;
  final String? label;

  @override
  Widget build(BuildContext context) {
    final box = Container(
      width: size,
      height: size,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: filled ? C.teal : (dashed ? Colors.transparent : C.tealLight),
        borderRadius: BorderRadius.circular(size * 0.28),
        border: dashed ? Border.all(color: C.gold, width: 1.5) : null,
      ),
      child: Text(
        char,
        style: arab(size * 0.55, color: filled ? Colors.white : (dashed ? C.goldDark : C.teal), height: 1.2),
      ),
    );
    if (onTap == null) return box;
    return Semantics(
      button: true,
      label: label,
      child: InkWell(borderRadius: BorderRadius.circular(size * 0.28), onTap: onTap, child: box),
    );
  }
}

class Chip2 extends StatelessWidget {
  const Chip2(this.text, {super.key, this.gold = false});
  final String text;
  final bool gold;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
    decoration: BoxDecoration(color: gold ? C.goldLight : C.tealLight, borderRadius: BorderRadius.circular(12)),
    child: Text(
      text,
      style: TextStyle(
        fontSize: 13,
        fontWeight: gold ? FontWeight.w700 : FontWeight.w600,
        color: gold ? C.goldInk : C.tealDark,
      ),
    ),
  );
}

class Note extends StatelessWidget {
  const Note(this.child, {super.key, this.icon = Icons.info_outline});
  final Widget child;
  final IconData icon;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
    decoration: BoxDecoration(color: C.goldLight, borderRadius: BorderRadius.circular(14)),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 18, color: C.goldInk),
        const SizedBox(width: 10),
        Expanded(
          child: DefaultTextStyle.merge(
            style: const TextStyle(fontSize: 13, height: 1.55, color: C.goldInk),
            child: child,
          ),
        ),
      ],
    ),
  );
}

/// Badge kecil "belum divalidasi guru".
class ValidasiBadge extends StatelessWidget {
  const ValidasiBadge({super.key, required this.tervalidasi});
  final bool tervalidasi;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
    decoration: BoxDecoration(color: tervalidasi ? C.tealLight : C.goldLight, borderRadius: BorderRadius.circular(8)),
    child: Text(
      tervalidasi ? 'Divalidasi pengajar' : 'Belum divalidasi pengajar',
      style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: tervalidasi ? C.tealDark : C.goldInk),
    ),
  );
}

/// Pemutar klip guru melalui YouTube IFrame Player resmi (tanpa mengunduh video).
/// Awalnya hanya menampilkan thumbnail dengan tombol putar; pemutar resmi baru dimuat
/// saat diketuk, dan ketukan itu langsung memulai pemutaran.
class KlipGuru extends StatefulWidget {
  const KlipGuru({super.key, required this.videoId});
  final String videoId;

  @override
  State<KlipGuru> createState() => KlipGuruState();
}

class KlipGuruState extends State<KlipGuru> {
  YoutubePlayerController? _c;

  /// Putar dari detik tertentu; null = dari awal.
  Future<void> putar({double? mulai}) async {
    final c = _c;
    if (c == null) {
      setState(
        () => _c = YoutubePlayerController.fromVideoId(
          videoId: widget.videoId,
          autoPlay: true,
          startSeconds: mulai,
          params: const YoutubePlayerParams(
            showFullscreenButton: true,
            strictRelatedVideos: true,
            showVideoAnnotations: false,
          ),
        ),
      );
      return;
    }
    await c.seekTo(seconds: mulai ?? 0, allowSeekAhead: true);
    await c.playVideo();
  }

  @override
  void dispose() {
    _c?.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final c = _c;
    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: ColoredBox(
        color: C.ink,
        child: c != null
            ? YoutubePlayer(controller: c, aspectRatio: 16 / 9)
            : AspectRatio(
                aspectRatio: 16 / 9,
                child: Semantics(
                  button: true,
                  label: 'Putar video rujukan',
                  child: InkWell(
                    onTap: putar,
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        Image.network(
                          'https://i.ytimg.com/vi/${widget.videoId}/hqdefault.jpg',
                          fit: BoxFit.cover,
                          webHtmlElementStrategy: WebHtmlElementStrategy.fallback,
                          errorBuilder: (_, _, _) => const SizedBox.shrink(),
                        ),
                        const ColoredBox(color: Color(0x33000000)),
                        Center(
                          child: Container(
                            width: 60,
                            height: 60,
                            decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle),
                            child: const Icon(Icons.play_arrow, size: 32, color: C.ink),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}

class VideoKosong extends StatelessWidget {
  const VideoKosong({super.key});

  @override
  Widget build(BuildContext context) => Container(
    height: 150,
    alignment: Alignment.center,
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(color: C.ink, borderRadius: BorderRadius.circular(20)),
    child: const Text(
      'Video rujukan untuk huruf ini belum tersedia di playlist kanal Al-Andalasy.',
      textAlign: TextAlign.center,
      style: TextStyle(color: Color(0xFFC9CEDA), fontSize: 13, height: 1.5),
    ),
  );
}

/// Navigasi bawah empat tab.
class BottomNav extends StatelessWidget {
  const BottomNav({super.key, required this.location});
  final String location;

  @override
  Widget build(BuildContext context) {
    const items = [
      ('/', 'Beranda', Icons.home_outlined),
      ('/peta', 'Tahsin', Icons.map_outlined),
      ('/mushaf', 'Mushaf', Icons.menu_book_outlined),
      ('/profil', 'Profil', Icons.person_outline),
    ];
    return Container(
      height: 72,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: C.line)),
      ),
      child: Row(
        children: [
          for (final (path, label, icon) in items)
            Expanded(
              child: Semantics(
                selected: location == path,
                child: InkWell(
                  onTap: () => context.go(path),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(icon, color: location == path ? C.teal : C.grey),
                      const SizedBox(height: 4),
                      Text(
                        label,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: location == path ? FontWeight.w700 : FontWeight.w500,
                          color: location == path ? C.teal : C.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

/// Tombol utama penuh lebar.
class BigButton extends StatelessWidget {
  const BigButton(this.label, {super.key, this.icon, this.onPressed, this.outline = false, this.color = C.teal});
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final bool outline;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final child = Row(
      mainAxisAlignment: MainAxisAlignment.center,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (icon != null) ...[Icon(icon, size: 20), const SizedBox(width: 10)],
        Flexible(child: Text(label, textAlign: TextAlign.center)),
      ],
    );
    final shape = RoundedRectangleBorder(borderRadius: BorderRadius.circular(16));
    const ts = TextStyle(fontFamily: 'Jakarta', fontSize: 15, fontWeight: FontWeight.w700);
    return SizedBox(
      width: double.infinity,
      height: 54,
      child: outline
          ? OutlinedButton(
              onPressed: onPressed,
              style: OutlinedButton.styleFrom(
                foregroundColor: color,
                side: BorderSide(color: color, width: 1.5),
                shape: shape,
                textStyle: ts,
              ),
              child: child,
            )
          : FilledButton(
              onPressed: onPressed,
              style: FilledButton.styleFrom(backgroundColor: color, shape: shape, textStyle: ts),
              child: child,
            ),
    );
  }
}
