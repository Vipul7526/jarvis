// Orbital Instrument direction: a calm mobile control surface with honest readiness states and copper signal accents.
import 'package:flutter/material.dart';

void main() => runApp(const JarvisApp());

class JarvisApp extends StatelessWidget {
  const JarvisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'J.A.R.V.I.S.',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0C1116),
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFD7814A), brightness: Brightness.dark),
        fontFamily: 'monospace',
      ),
      home: const ReadinessPage(),
    );
  }
}

class ReadinessPage extends StatelessWidget {
  const ReadinessPage({super.key});

  @override
  Widget build(BuildContext context) {
    final rows = <({String label, String state})>[
      (label: 'AUTH / PAIRING', state: 'VERIFIED'),
      (label: 'OFFLINE CORE', state: 'SCAFFOLDED'),
      (label: 'VOICE / WAKE WORD', state: 'PLANNED'),
      (label: 'DESKTOP ROUTE', state: 'PLANNED'),
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('J.A.R.V.I.S. / CONTROL'), backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const Text('CHECK THE SIGNAL', style: TextStyle(color: Color(0xFFD7814A), letterSpacing: 2, fontSize: 12)),
          const SizedBox(height: 18),
          const Text('One assistant.\nEvery authorized surface.', style: TextStyle(fontSize: 40, height: .98, fontWeight: FontWeight.w700)),
          const SizedBox(height: 18),
          Text('The mobile client will pair with authorized devices and route commands through the secure control plane.', style: TextStyle(color: Colors.grey.shade400, height: 1.6)),
          const SizedBox(height: 34),
          ...rows.map((row) => Card(
                color: const Color(0xFF111922),
                shape: RoundedRectangleBorder(side: const BorderSide(color: Color(0x243F4B55)), borderRadius: BorderRadius.circular(2)),
                child: ListTile(
                  title: Text(row.label, style: const TextStyle(fontSize: 12)),
                  trailing: Text(row.state, style: TextStyle(color: row.state == 'VERIFIED' ? const Color(0xFF9BD485) : const Color(0xFFD7814A), fontSize: 10)),
                ),
              )),
          const SizedBox(height: 20),
          FilledButton.icon(onPressed: null, icon: const Icon(Icons.link), label: const Text('PAIR A DEVICE WHEN AVAILABLE')),
        ],
      ),
    );
  }
}
