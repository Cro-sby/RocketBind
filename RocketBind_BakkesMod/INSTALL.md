# RocketBind Installation Guide

## Installation Steps

1. **Copy the plugin DLL**
   - Copy `RocketBind_BakkesMod\Release\RocketBind.dll` to your BakkesMod plugins folder:
   - Default location: `%APPDATA%\bakkesmod\bakkesmod\plugins\`
   - Full path: `C:\Users\YourUsername\AppData\Roaming\bakkesmod\bakkesmod\plugins\`

2. **Launch Rocket League with BakkesMod**
   - Start BakkesMod
   - Launch Rocket League

3. **Load the plugin**
   - Press **F2** to open the BakkesMod console
   - Type: `plugin load rocketbind`
   - Press Enter

4. **Open the plugin window**
   - Press **F2** to open the BakkesMod menu
   - Look for "RocketBind" in the plugins menu
   - Click to open the RocketBind window

## Usage

### Save a Preset
1. Configure your controller keybindings in Rocket League settings
2. Open RocketBind plugin window (F2 → Plugins → RocketBind)
3. Enter a name for your preset (e.g., "Aerial Build", "Ground Play")
4. Click "Save Current Keybindings"

### Load a Preset
1. Open RocketBind plugin window
2. Select a preset from the dropdown
3. Click "Load Keybindings"
4. Your keybindings will be instantly applied!

## Troubleshooting

### Plugin won't load
- Make sure you're using the **Release** version (not Debug)
- Check BakkesMod console (F6) for error messages
- Verify the DLL is in the correct plugins folder

### Can't see my presets
- Click "Refresh List" button
- Presets are saved in: `%APPDATA%\bakkesmod\bakkesmod\data\RocketBind\`

### Crashes on load
- Delete the old DLL and copy the new Release version
- Make sure BakkesMod is up to date
- Check that Visual Studio C++ Runtime is installed

## Important Notes

- **Always use the Release build** - Debug builds will crash Rocket League
- The plugin works in all game modes (Freeplay, Online, Training, etc.)
- Keybindings are saved as JSON files for easy backup
- The plugin only affects controller keybindings, not camera or sensitivity settings
