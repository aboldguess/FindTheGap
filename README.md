# FindTheGap

Prototype repository for a cross-platform augmented reality app that guides rail passengers through platform changes and interchanges.

## Code-First Approach
We use **Flutter** with the `ar_flutter_plugin` to achieve AR on both Android and iOS without relying on Unity's editor-heavy workflow.

## Repository Structure
- `mobile_app/` – Flutter client prototype.
- `TODO.md` – Project backlog.

## Automated Flutter Setup
Run the helper script to install Flutter and configure the environment automatically. A small GUI displays progress and falls back to alternative methods if the first attempt fails. Logging is written to `flutter_setup.log` for troubleshooting.

### Windows
```powershell
py -3 -m venv .venv
./.venv/Scripts/Activate.ps1
python flutter_env_setup.py
```

### Linux & Raspberry Pi
```bash
python3 -m venv .venv
source .venv/bin/activate
python flutter_env_setup.py
```

## Manual Setup

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
Enable developer mode and USB debugging on your phone, then:

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

### Programmatic Checks
Run static analysis to catch issues early:
```bash
cd mobile_app
flutter analyze
```

### Notes
- Use `--verbose` for extra debug output.
- Ensure mobile devices have developer mode enabled before running.
