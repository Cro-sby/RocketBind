# RocketBind

**Rocket League Preset Manager** - Create, manage, and instantly swap between multiple controller/keyboard configurations for Rocket League.

## Features

- 🎮 **Preset Management** - Create, edit, duplicate, and delete control presets
- 📥 **Import Current Settings** - Import your existing Rocket League configuration
- ✅ **Smart Validation** - Prevents invalid bindings and conflicts
- 🚀 **Auto Apply & Restart** - Automatically closes game, applies preset, and relaunches
- 🎨 **Modern UI** - Clean, dark-themed interface with Rocket League-inspired colors
- 💾 **Auto Backup** - Automatically backs up your original config file

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Creating a Preset
1. Click "Import" to import your current Rocket League settings
2. Or click "New" to create a preset from scratch

### Editing Bindings
1. Select a preset from the sidebar
2. View and edit Gamepad or Keyboard/Mouse bindings
3. Click "Save Changes" to save modifications

### Applying a Preset
1. Select the preset you want to use
2. Choose your platform (Steam or Epic)
3. Click "APPLY & RESTART"
4. The app will close Rocket League (if running), apply your preset, and relaunch the game

### Managing Presets
- **Duplicate**: Create a copy of an existing preset
- **Delete**: Remove a preset (requires confirmation)

## File Locations

- **Game Config**: `%USERPROFILE%\Documents\My Games\Rocket League\TAGame\Config\TAInput.ini`
- **Presets**: Stored in the `presets/` folder within the application directory
- **Backup**: Original config backed up as `TAInput.ini.bak`

## Requirements

- Windows 10/11
- Python 3.8+
- Rocket League (Steam or Epic Games version)

## Troubleshooting

### Settings revert after applying
If your settings keep reverting, disable Steam Cloud for Rocket League:
1. Right-click Rocket League in Steam
2. Properties → General
3. Uncheck "Keep game saves in the Steam Cloud"

### Config file is read-only
The app automatically removes the read-only attribute when applying presets.

## Tech Stack

- **Python** - Core logic and file handling
- **CustomTkinter** - Modern UI framework
- **psutil** - Process management

## License

MIT License - See LICENSE file for details

## Credits

Created for the Rocket League community by players who wanted better control preset management.
