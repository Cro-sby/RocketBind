# RocketBind - BakkesMod Plugin

**Keybinding Preset Manager for Rocket League**

RocketBind is a BakkesMod plugin that allows you to save and load controller keybinding configurations instantly, without modifying sensitivity, camera settings, or deadzones.

---

## Features

- 🎮 **Save Current Keybindings** - Capture your current controller bindings as a preset
- 📥 **Load Presets Instantly** - Apply any saved preset with one click
- 🔄 **Preset Management** - Create multiple presets for different playstyles
- ✅ **Safe & Simple** - Only modifies button bindings, never touches sensitivity or camera
- 💾 **JSON Format** - Easy to read, edit, and share preset files

---

## Prerequisites

1. **BakkesMod** - Download from [bakkesmod.com](https://bakkesmod.com)
2. **Visual Studio 2019/2022** - With "Desktop development with C++"
3. **CMake 3.10+** - Download from [cmake.org](https://cmake.org/download/)
4. **BakkesMod SDK** - Located at: `C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\BakkesModSDK-master`

---

## Setup Instructions

### 1. Download nlohmann/json

Download the single-header JSON library:

1. Go to: https://github.com/nlohmann/json/releases
2. Download `json.hpp` from the latest release
3. Place `json.hpp` in this folder: `RocketBind_BakkesMod/`

### 2. Verify SDK Path

Make sure the BakkesMod SDK is at:
```
C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\BakkesModSDK-master
```

The SDK should contain:
- `include/` folder with header files
- `lib/` folder with `pluginsdk.lib`

---

## Build Instructions

### Option 1: Command Line (Recommended)

1. Open **"x64 Native Tools Command Prompt for VS 2022"** (search in Start menu)

2. Navigate to the plugin folder:
   ```cmd
   cd "C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\RocketBind_BakkesMod"
   ```

3. Create build directory and generate project:
   ```cmd
   mkdir build
   cd build
   cmake .. -G "Visual Studio 17 2022" -A x64
   ```

4. Build the plugin:
   ```cmd
   cmake --build . --config Release
   ```

5. The compiled DLL will be in: `Release/RocketBind.dll`

### Option 2: Visual Studio IDE

1. Open **"x64 Native Tools Command Prompt for VS 2022"**
2. Navigate to plugin folder and run:
   ```cmd
   cd "C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\RocketBind_BakkesMod"
   mkdir build
   cd build
   cmake .. -G "Visual Studio 17 2022" -A x64
   ```
3. Open `build/RocketBind.sln` in Visual Studio
4. Set build configuration to **Release** (top toolbar)
5. Build → Build Solution (or press F7)

---

## Installation

1. Build the plugin using instructions above
2. Find `RocketBind.dll` in the `Release/` folder
3. Copy it to your BakkesMod plugins folder:
   ```
   %APPDATA%\bakkesmod\bakkesmod\plugins\
   ```
4. Launch Rocket League with BakkesMod
5. Open BakkesMod console (F6) and type:
   ```
   plugin load RocketBind
   ```

---

## Usage

### Accessing the Plugin

1. Launch Rocket League with BakkesMod injected
2. Press **F2** to open BakkesMod menu
3. Click on **"RocketBind"** in the plugins tab

### Saving a Preset

1. Configure your controller bindings in Rocket League settings
2. Open RocketBind in BakkesMod menu (F2)
3. Enter a name for your preset (e.g., "Competitive", "Freestyle", "Default")
4. Click **"Save Current Keybindings"**
5. You'll see a toast notification confirming the save

### Loading a Preset

1. Open RocketBind in BakkesMod menu (F2)
2. Select a preset from the dropdown
3. Click **"Load Keybindings"**
4. Your controller bindings will update instantly!

### Managing Presets

- **Refresh List** - Click to scan for new preset files
- **Edit Presets** - Edit `.json` files directly in: `%APPDATA%\bakkesmod\bakkesmod\data\RocketBind\`
- **Share Presets** - Copy `.json` files to share with friends

---

## Preset File Format

Presets are stored as JSON files in:
```
%APPDATA%\bakkesmod\bakkesmod\data\RocketBind\
```

Example `sample_preset.json`:
```json
{
  "bindings": {
    "XboxTypeS_A": "Boost",
    "XboxTypeS_B": "Jump",
    "XboxTypeS_X": "AirRollLeft",
    "XboxTypeS_RightTrigger": "Throttle"
  }
}
```

### Supported Keys

- `XboxTypeS_A`, `XboxTypeS_B`, `XboxTypeS_X`, `XboxTypeS_Y`
- `XboxTypeS_LeftShoulder`, `XboxTypeS_RightShoulder`
- `XboxTypeS_LeftTrigger`, `XboxTypeS_RightTrigger`
- `XboxTypeS_LeftThumbStick`, `XboxTypeS_RightThumbStick`
- `XboxTypeS_Start`, `XboxTypeS_Back`
- `XboxTypeS_DPad_Up`, `XboxTypeS_DPad_Down`, `XboxTypeS_DPad_Left`, `XboxTypeS_DPad_Right`

---

## Troubleshooting

### Build Errors

**"Cannot find pluginsdk.lib"**
- Check that SDK path in `CMakeLists.txt` is correct
- Verify `lib/pluginsdk.lib` exists in the SDK folder

**"Cannot find json.hpp"**
- Download it from: https://github.com/nlohmann/json/releases
- Place it in the `RocketBind_BakkesMod/` folder

**"CMake not recognized"**
- Restart your terminal after installing CMake
- Or use the full path: `"C:\Program Files\CMake\bin\cmake.exe"`

### Plugin Errors

**"Plugin failed to load"**
- Make sure you built in Release mode (not Debug)
- Check BakkesMod console (F6) for error messages
- Verify the DLL is in: `%APPDATA%\bakkesmod\bakkesmod\plugins\`

**"No presets found"**
- The plugin creates the folder automatically on first run
- Check: `%APPDATA%\bakkesmod\bakkesmod\data\RocketBind\`
- Try saving a new preset to create the directory

**"Bindings not applying"**
- Make sure you're in freeplay or a match (not main menu)
- Check the preset JSON file format is correct
- Try refreshing the preset list

---

## Development

### Project Structure

```
RocketBind_BakkesMod/
├── CMakeLists.txt          # Build configuration
├── RocketBind.h            # Header file with class definition
├── RocketBind.cpp          # Core logic (save/load/init)
├── RocketBindGUI.cpp       # ImGui UI rendering
├── json.hpp                # nlohmann/json library
├── sample_preset.json      # Example preset
└── README.md               # This file
```

### Modifying the Plugin

1. Edit source files (`.h`, `.cpp`)
2. Rebuild:
   ```cmd
   cd build
   cmake --build . --config Release
   ```
3. Copy new DLL to plugins folder
4. In RL, type in console (F6):
   ```
   plugin unload RocketBind
   plugin load RocketBind
   ```

### Adding More Keys

Edit the `controllerKeys` vector in `RocketBind.h` to include additional inputs.

---

## FAQ

**Q: Does this work with PlayStation controllers?**  
A: Currently only Xbox inputs are supported. PS4/PS5 support coming soon.

**Q: Can I share presets with friends?**  
A: Yes! Just share the `.json` file from the data directory.

**Q: Will this get me banned?**  
A: No. BakkesMod is allowed by Psyonix and only works in freeplay/custom games/replays.

**Q: Does this change my sensitivity or camera?**  
A: No. This plugin ONLY modifies button bindings, nothing else.

---

## Support

- **BakkesMod Discord**: https://discord.gg/bakkesmod
- **Issues**: Report bugs or request features on GitHub

---

## Credits

- Created for the Rocket League community
- Built with the BakkesMod SDK
- Uses nlohmann/json for JSON parsing

---

## License

MIT License - Free to use, modify, and distribute.

---

**Happy binding! 🚗💨⚽**
