import 'package:flutter_test/flutter_test.dart';
import 'package:jarvis_client/main.dart';

void main() {
  testWidgets('readiness surface distinguishes verified and planned states', (tester) async {
    await tester.pumpWidget(const JarvisApp());
    expect(find.text('AUTH / PAIRING'), findsOneWidget);
    expect(find.text('VERIFIED'), findsOneWidget);
    expect(find.text('PLANNED'), findsWidgets);
  });
}
