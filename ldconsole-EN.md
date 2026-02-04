# dnconsole Command Line Tool Manual

`dnconsole` is the command-line control tool for **LDPlayer (Android Emulator)**, used for batch management of emulator instances.

---

## Basic Syntax

```
dnconsole <command> [parameters]
```

**Common Parameters:**

- `--name mnq_name`: Specify emulator by name
- `--index mnq_idx`: Specify emulator by index (starting from 0)

---

## Command Categories

### 1. Emulator Lifecycle Management

| Command | Description | Example |
|---------|-------------|---------|
| `launch` | Start emulator | `dnconsole launch --name MyPhone` |
| `launchex` | Start emulator and run app | `dnconsole launchex --index 0 --packagename com.example` |
| `quit` | Close emulator | `dnconsole quit --index 0` |
| `quitall` | Close all emulators | `dnconsole quitall` |
| `reboot` | Restart emulator | `dnconsole reboot --name MyPhone` |

---

### 2. Emulator Query

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all emulators | `dnconsole list` |
| `list2` | List all emulators (detailed info) | `dnconsole list2` |
| `runninglist` | List running emulators | `dnconsole runninglist` |
| `isrunning` | Check if emulator is running | `dnconsole isrunning --index 0` |

---

### 3. Emulator Management

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Create new emulator | `dnconsole add --name NewPhone` |
| `copy` | Clone emulator | `dnconsole copy --name Clone1 --from 0` |
| `remove` | Delete emulator | `dnconsole remove --name OldPhone` |
| `rename` | Rename emulator | `dnconsole rename --index 0 --title NewName` |

---

### 4. Emulator Configuration (modify)

```bash
dnconsole modify <--name mnq_name | --index mnq_idx> [options]
```

#### Hardware Settings

| Option | Description | Values |
|--------|-------------|--------|
| `--resolution` | Screen resolution | `width,height,DPI` (e.g., `1280,720,240`) |
| `--cpu` | CPU cores | `1`, `2`, `3`, `4` |
| `--memory` | Memory (MB) | `256`, `512`, `768`, `1024`, `1536`, `2048`, `4096`, `8192` |

#### Device Information

| Option | Description | Values |
|--------|-------------|--------|
| `--manufacturer` | Manufacturer | e.g., `asus` |
| `--model` | Device model | e.g., `ASUS_Z00DUO` |
| `--pnumber` | Phone number | e.g., `13800000000` |

#### Device Identifiers

| Option | Description | Values |
|--------|-------------|--------|
| `--imei` | IMEI | `auto` or specific value (e.g., `865166023949731`) |
| `--imsi` | IMSI | `auto` or specific value (e.g., `460000000000000`) |
| `--simserial` | SIM serial number | `auto` or specific value (e.g., `89860000000000000000`) |
| `--androidid` | Android ID | `auto` or 16-digit hex (e.g., `0123456789abcdef`) |
| `--mac` | MAC address | `auto` or 12-digit hex (e.g., `000000000000`) |

#### Display Settings

| Option | Description | Values |
|--------|-------------|--------|
| `--autorotate` | Auto-rotate | `1` enable / `0` disable |
| `--lockwindow` | Lock window | `1` enable / `0` disable |

---

### 5. App Management

| Command | Description | Parameters |
|---------|-------------|------------|
| `installapp` | Install app | `--filename <apk_path>` or `--packagename <package>` |
| `uninstallapp` | Uninstall app | `--packagename <package>` |
| `runapp` | Launch app | `--packagename <package>` |
| `killapp` | Terminate app | `--packagename <package>` |

**Examples:**

```bash
# Install from local APK
dnconsole installapp --index 0 --filename "C:\Downloads\app.apk"

# Install from store (by package name)
dnconsole installapp --index 0 --packagename com.example.app

# Launch app
dnconsole runapp --index 0 --packagename com.example.app

# Uninstall app
dnconsole uninstallapp --index 0 --packagename com.example.app
```

---

### 6. File Operations

| Command | Description | Parameters |
|---------|-------------|------------|
| `pull` | Pull file from emulator to local | `--remote <emulator_path> --local <local_path>` |
| `push` | Push local file to emulator | `--remote <emulator_path> --local <local_path>` |
| `backup` | Backup entire emulator | `--file <backup_path>` |
| `restore` | Restore emulator from backup | `--file <backup_path>` |
| `backupapp` | Backup specific app data | `--packagename <package> --file <path>` |
| `restoreapp` | Restore specific app data | `--packagename <package> --file <path>` |
| `scan` | Scan file to emulator media library | `--file <path>` |

**Examples:**

```bash
# Backup emulator
dnconsole backup --index 0 --file "D:\backup\phone0.ldbk"

# Restore emulator
dnconsole restore --index 0 --file "D:\backup\phone0.ldbk"

# Pull screenshot from emulator
dnconsole pull --index 0 --remote /sdcard/DCIM/screenshot.png --local "C:\screenshots\"

# Push file to emulator
dnconsole push --index 0 --local "C:\files\data.txt" --remote /sdcard/Download/
```

---

### 7. System Operations

| Command | Description | Parameters |
|---------|-------------|------------|
| `locate` | Set virtual GPS location | `--LLI <longitude,latitude>` |
| `adb` | Execute ADB command | `--command <command_string>` |
| `setprop` | Set system property | `--key <property> --value <value>` |
| `getprop` | Get system property | `--key <property>` (optional) |
| `downcpu` | Limit CPU usage | `--rate <0~100>` |
| `action` | Execute simulated action | `--key <name> --value <value>` |

**Examples:**

```bash
# Set location to Tokyo
dnconsole locate --index 0 --LLI 139.6917,35.6895

# Execute ADB shell command
dnconsole adb --index 0 --command "shell input tap 500 500"

# Simulate key press
dnconsole adb --index 0 --command "shell input keyevent 4"

# Get system property
dnconsole getprop --index 0 --key ro.product.model

# Limit CPU usage to 50%
dnconsole downcpu --index 0 --rate 50
```

---

### 8. Window Management

| Command | Description |
|---------|-------------|
| `sortWnd` | Auto-arrange all emulator windows |
| `zoomIn` | Zoom in window |
| `zoomOut` | Zoom out window |

---

### 9. Global Settings

```bash
dnconsole globalsetting [options]
```

| Option | Description | Values |
|--------|-------------|--------|
| `--fps` | Frame rate limit | `0` ~ `60` |
| `--audio` | Audio toggle | `1` on / `0` off |
| `--fastplay` | Fast play mode | `1` on / `0` off |
| `--cleanmode` | Clean mode | `1` on / `0` off |

---

## Common Usage Examples

### Batch Launch Emulators

```bash
dnconsole launch --index 0
dnconsole launch --index 1
dnconsole launch --index 2
```

### Batch Install App

```bash
for /L %i in (0,1,5) do dnconsole installapp --index %i --filename "C:\app.apk"
```

### Automation Script Example

```bash
# Launch emulator → Wait for boot → Run app
dnconsole launch --index 0
timeout /t 30
dnconsole runapp --index 0 --packagename com.example.app
```

### Set Different Locations for Multiple Emulators

```bash
dnconsole locate --index 0 --LLI -122.4194,37.7749   # San Francisco
dnconsole locate --index 1 --LLI -74.0060,40.7128    # New York
dnconsole locate --index 2 --LLI -0.1276,51.5074    # London
```

---

## Notes

1. **Paths containing spaces must be wrapped in quotes**
2. **Emulator index starts from 0**
3. **Some commands require the emulator to be running**
4. **ADB commands require emulator to be fully booted**

---

## Reference

- LDPlayer Official Documentation
- Command line tool location: `LDPlayer_Install_Directory\ldconsole.exe` or `dnconsole.exe`
