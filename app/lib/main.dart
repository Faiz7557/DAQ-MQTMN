import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import 'data/materi.dart';
import 'data/progress.dart';
import 'data/quran.dart';
import 'screens/home.dart';
import 'screens/lesson.dart';
import 'screens/mushaf.dart';
import 'screens/peta.dart';
import 'screens/practice.dart';
import 'screens/profile.dart';
import 'screens/similar.dart';
import 'theme.dart';
import 'widgets/common.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // ?demo=1 (web) mengisi progres contoh untuk demo video dan tangkapan layar.
  final demo = kIsWeb && Uri.base.queryParameters['demo'] == '1';
  final results = await Future.wait([Materi.load(), Quran.load()]);
  final progress = Progress();
  await progress.init(demo: demo);
  runApp(MakhrajApp(materi: results[0] as Materi, quran: results[1] as Quran, progress: progress));
}

GoRouter buatRouter() => GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) => Scaffold(
        body: SafeArea(child: child),
        bottomNavigationBar: SafeArea(top: false, child: BottomNav(location: state.uri.path)),
      ),
      routes: [
        GoRoute(path: '/', builder: (_, _) => const HomeScreen()),
        GoRoute(
          path: '/peta',
          builder: (_, s) => PetaScreen(areaAwal: s.uri.queryParameters['area']),
        ),
        GoRoute(path: '/mushaf', builder: (_, _) => const MushafListScreen()),
        GoRoute(path: '/profil', builder: (_, _) => const ProfileScreen()),
      ],
    ),
    GoRoute(
      path: '/huruf/:id',
      builder: (_, s) => LessonScreen(id: s.pathParameters['id']!),
    ),
    GoRoute(
      path: '/latihan/:id',
      builder: (_, s) => PracticeScreen(id: s.pathParameters['id']!),
    ),
    GoRoute(path: '/mirip', builder: (_, _) => const SimilarListScreen()),
    GoRoute(
      path: '/mirip/:i',
      builder: (_, s) => SimilarScreen(index: int.parse(s.pathParameters['i']!)),
    ),
    GoRoute(
      path: '/mushaf/:n',
      builder: (_, s) => MushafReaderScreen(
        n: int.parse(s.pathParameters['n']!).clamp(1, 114),
        hurufAwal: s.uri.queryParameters['huruf'],
      ),
    ),
  ],
);

class MakhrajApp extends StatefulWidget {
  const MakhrajApp({super.key, required this.materi, required this.quran, required this.progress});
  final Materi materi;
  final Quran quran;
  final Progress progress;

  @override
  State<MakhrajApp> createState() => _MakhrajAppState();
}

class _MakhrajAppState extends State<MakhrajApp> {
  final _router = buatRouter();

  @override
  void dispose() {
    _router.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider.value(value: widget.materi),
        Provider.value(value: widget.quran),
        ChangeNotifierProvider.value(value: widget.progress),
      ],
      child: MaterialApp.router(
        title: 'Makhraj',
        debugShowCheckedModeBanner: false,
        theme: buildTheme(),
        routerConfig: _router,
        builder: (context, child) => _bingkai(context, child!),
      ),
    );
  }
}

/// ?frame=390x844 (web) merender aplikasi dalam bingkai ponsel berukuran tetap
/// di pojok kiri atas, dipakai tool/capture.py untuk tangkapan layar proposal.
Widget _bingkai(BuildContext context, Widget child) {
  final f = kIsWeb ? Uri.base.queryParameters['frame'] : null;
  final m = f == null ? null : RegExp(r'^(\d+)x(\d+)$').firstMatch(f);
  if (m == null) return child;
  final size = Size(double.parse(m.group(1)!), double.parse(m.group(2)!));
  return ColoredBox(
    color: const Color(0xFF808080),
    child: Align(
      alignment: Alignment.topLeft,
      child: SizedBox.fromSize(
        size: size,
        child: MediaQuery(
          data: MediaQuery.of(context).copyWith(size: size),
          child: ClipRect(child: child),
        ),
      ),
    ),
  );
}
