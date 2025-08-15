# Mobile AR Prototype

This directory contains a Flutter-based prototype for the FindTheGap AR client.

## Structure
- `pubspec.yaml` – Flutter package configuration and dependencies.
- `lib/main.dart` – Application entry point and initial AR scaffold.
- `run_android.sh` – Helper script to deploy to an Android device.

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

### Android Device
Connect your phone with USB debugging enabled and run:

#### Linux & Raspberry Pi
```bash
cd mobile_app
./run_android.sh [device-id]
```

#### Windows
```powershell
cd mobile_app
flutter pub get
flutter run -d <device-id>
```

### Notes
- Use `--verbose` for detailed debug logs.
- Specify devices with `flutter devices`.
