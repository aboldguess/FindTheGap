# Mobile AR Prototype

This directory contains a Flutter-based prototype for the FindTheGap AR client.

## Structure
- `pubspec.yaml` – Flutter package configuration and dependencies.
- `lib/main.dart` – Application entry point and initial AR scaffold.

## Quick Start

### Prerequisites
- Flutter SDK (latest stable version).
- Android Studio or Xcode for device emulators.

### Linux & Raspberry Pi
```bash
sudo snap install flutter --classic
cd mobile_app
flutter pub get
flutter run -d linux  # or specify connected device
```

### Windows
```powershell
winget install -e --id=Flutter.Flutter
cd mobile_app
flutter pub get
flutter run -d windows # or specify connected device
```

### Notes
- Use `--verbose` for detailed debug logs.
- Specify devices with `flutter devices`.
