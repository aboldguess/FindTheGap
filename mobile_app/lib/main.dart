/*
# Main AR Entry Point

This file bootstraps the Flutter-based AR prototype for the FindTheGap project.

## Structure
- `main()` → launches the `FindTheGapApp`.
- `FindTheGapApp` → root widget configuring theming and the home page.
- `ARHomePage` → stateful widget hosting the AR view and on‑screen tips.
- `_ARHomePageState` → manages AR session setup and tap gestures.

## Usage
Run the app on an Android device to see plane detection. Tap a detected plane to
place a cube marker. Debug information is printed to the console.
*/

import 'package:ar_flutter_plugin/ar_flutter_plugin.dart';
import 'package:ar_flutter_plugin/datatypes/config_planedetection.dart';
import 'package:ar_flutter_plugin/datatypes/node_types.dart';
import 'package:ar_flutter_plugin/managers/ar_anchor_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_location_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_object_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_session_manager.dart';
import 'package:ar_flutter_plugin/models/ar_hittest_result.dart';
import 'package:ar_flutter_plugin/models/ar_node.dart';
import 'package:flutter/material.dart';
import 'package:vector_math/vector_math_64.dart' as vm;

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

/// Home page containing the AR view and user instructions.
class ARHomePage extends StatefulWidget {
  const ARHomePage({super.key});

  @override
  State<ARHomePage> createState() => _ARHomePageState();
}

class _ARHomePageState extends State<ARHomePage> {
  late ARSessionManager _sessionManager;
  late ARObjectManager _objectManager;
  ARNode? _placedNode;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Find The Gap Prototype'),
      ),
      body: Stack(
        children: [
          ARView(
            onARViewCreated: _onARViewCreated,
            planeDetectionConfig: PlaneDetectionConfig.horizontal,
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              color: Colors.black54,
              padding: const EdgeInsets.all(8),
              child: const Text(
                'Move your device to detect planes.\nTap to place a marker.',
                style: TextStyle(color: Colors.white),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _onARViewCreated(
    ARSessionManager sessionManager,
    ARObjectManager objectManager,
    ARAnchorManager anchorManager,
    ARLocationManager locationManager,
  ) async {
    _sessionManager = sessionManager;
    _objectManager = objectManager;

    await _sessionManager.onInitialize(
      showFeaturePoints: false,
      showPlanes: true,
      showWorldOrigin: true,
      handleTaps: true,
    );
    await _objectManager.onInitialize();

    _sessionManager.onPlaneOrPointTap = _onPlaneTap;
    debugPrint('AR session initialized');
  }

  Future<void> _onPlaneTap(List<ARHitTestResult> hits) async {
    if (hits.isEmpty) return;
    final firstHit = hits.first;

    // Remove previously placed node for clarity.
    if (_placedNode != null) {
      await _objectManager.removeNode(_placedNode!);
      _placedNode = null;
    }

    final node = ARNode(
      type: NodeType.webGLB,
      uri:
          'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Cube/glTF-Binary/Cube.glb',
      scale: vm.Vector3.all(0.2),
      position: firstHit.worldTransform.getTranslation(),
    );

    final didAdd = await _objectManager.addNode(node);
    if (didAdd == true) {
      _placedNode = node;
      debugPrint('Placed cube at: ${node.position}');
    } else {
      debugPrint('Failed to add node');
    }
  }

  @override
  void dispose() {
    _sessionManager.dispose();
    super.dispose();
  }
}
