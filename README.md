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

## Run the Prototype

After the setup script completes, launch the augmented-reality demo with these steps.

### Linux & Raspberry Pi

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Enter the Flutter project:
   ```bash
   cd mobile_app
   ```
3. Fetch dependencies:
   ```bash
   flutter pub get
   ```
4. Run on the desktop (replace `linux` with a device ID from `flutter devices` if needed):
   ```bash
   flutter run -d linux
   ```

### Windows

1. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Enter the Flutter project:
   ```powershell
   cd mobile_app
   ```
3. Fetch dependencies:
   ```powershell
   flutter pub get
   ```
4. Run on the desktop (replace `windows` with a device ID from `flutter devices` if needed):
   ```powershell
   flutter run -d windows
   ```

### Android Phones

1. Enable developer mode and USB debugging on the phone.
2. Connect the phone via USB and verify it appears:
   ```bash
   flutter devices
   ```
3. Run the app on the phone:
   ```bash
   flutter run -d <device-id>
   ```

## Manual Setup

If the automated script cannot install Flutter, use these manual commands and then follow **Run the Prototype** above.

### Linux & Raspberry Pi
```bash
sudo snap install flutter --classic
```

### Windows
```powershell
winget install -e --id=Flutter.Flutter
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
