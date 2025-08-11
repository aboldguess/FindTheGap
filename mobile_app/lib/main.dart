/*
# Main AR Entry Point

This file bootstraps the Flutter-based AR prototype for the FindTheGap project.

## Structure
- `main()` initializes the `FindTheGapApp`.
- `FindTheGapApp` sets up basic theming and routes.
- `ARHomePage` provides a placeholder screen where the AR view will live.

## TODO
- [ ] Integrate `ARView` from `ar_flutter_plugin` into `ARHomePage`.
- [ ] Fetch live train data from backend service.
- [ ] Implement station layout rendering.
- [ ] Add optional user login and profile management.
- [ ] Replace placeholder UI with professional design and accessibility options.
*/

import 'package:flutter/material.dart';

/// Application entry point.
void main() {
  runApp(const FindTheGapApp());
}

/// Root widget for the AR prototype app.
class FindTheGapApp extends StatelessWidget {
  const FindTheGapApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Find The Gap AR',
      debugShowCheckedModeBanner: false,
      home: const ARHomePage(),
    );
  }
}

/// Placeholder home page that will host the AR scene.
class ARHomePage extends StatefulWidget {
  const ARHomePage({super.key});

  @override
  State<ARHomePage> createState() => _ARHomePageState();
}

class _ARHomePageState extends State<ARHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Find The Gap Prototype'),
      ),
      body: const Center(
        child: Text(
          'AR view coming soon.\nSelect your train to begin.',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
