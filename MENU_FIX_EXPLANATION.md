# RocketBind Menu Fix - Complete Explanation

## The Problem

The plugin was loading successfully but **no menu appeared anywhere** - not in F2, not via console commands, nowhere.

## Root Cause Analysis

After analyzing the working RocketPlugin source code, I discovered the critical missing piece:

### What RocketPlugin Does (that we were NOT doing):

In `RocketPlugin.cpp` lines 943-946:
```cpp
// Set the window bind to the default keybind if is not set.
if (!IsGUIWindowBound(GetMenuName())) {
    cvarManager->setBind(DEFAULT_GUI_KEYBIND, "togglemenu " + GetMenuName());
    BM_LOG("Set window keybind to {:s}", DEFAULT_GUI_KEYBIND);
}
```

**This code:**
1. Checks if the menu already has a keybind registered in BakkesMod's `binds.cfg` file
2. If NOT found, it automatically binds a key (Home key in RocketPlugin, F6 in our case) to the command `togglemenu rocketbind`
3. This is what actually makes the menu accessible!

### The Helper Function

RocketPlugin also has this helper function (lines 884-900):
```cpp
bool IsGUIWindowBound(const std::string& windowName)
{
    const std::string bind = "togglemenu " + windowName;
    std::ifstream file(BINDS_FILE_PATH);
    if (file.is_open()) {
        std::string line;
        while (getline(file, line)) {
            if (line.find(bind) != std::string::npos) {
                file.close();
                return true;
            }
        }
        file.close();
    }
    return false;
}
```

This checks the BakkesMod binds file (`%APPDATA%/bakkesmod/bakkesmod/cfg/binds.cfg`) to see if the menu already has a keybind.

## The Fix

I added to `RocketBind.cpp`:

1. **Helper function** to check if menu is already bound
2. **Keybind registration** in `onLoad()` that:
   - Checks if `togglemenu rocketbind` is already bound to a key
   - If not, binds F6 key to open the menu
   - Logs the binding for user confirmation

## Changes Made

### RocketBind.cpp

**Added at the top:**
```cpp
// Default keybind for the GUI (can be changed by user)
constexpr const char* DEFAULT_GUI_KEYBIND = "F6";

/// <summary>Checks if the GUI window is bound to a key.</summary>
bool IsGUIWindowBound(const std::string& windowName, const std::filesystem::path& bindsFilePath)
{
    const std::string bind = "togglemenu " + windowName;
    std::ifstream file(bindsFilePath);
    if (file.is_open()) {
        std::string line;
        while (getline(file, line)) {
            if (line.find(bind) != std::string::npos) {
                file.close();
                return true;
            }
        }
        file.close();
    }
    return false;
}
```

**Added in `onLoad()`:**
```cpp
// Get BakkesMod directories
fs::path bakkesModFolder = gameWrapper->GetBakkesModPath();
fs::path bindsFilePath = bakkesModFolder / "cfg" / "binds.cfg";

// Set the window bind to the default keybind if it is not set
if (!IsGUIWindowBound(GetMenuName(), bindsFilePath))
{
    cvarManager->setBind(DEFAULT_GUI_KEYBIND, "togglemenu " + GetMenuName());
    cvarManager->log("RocketBind: Set window keybind to " + std::string(DEFAULT_GUI_KEYBIND));
}
```

**Updated log messages** to reflect F6 keybind instead of F2 menu.

## How to Test

1. **Copy the new DLL:**
   - Source: `RocketBind_BakkesMod\Release\RocketBind.dll`
   - Destination: `%APPDATA%\bakkesmod\bakkesmod\plugins\RocketBind.dll`

2. **Launch Rocket League with BakkesMod**

3. **Open BakkesMod console** (F6 by default, or tilde key `~`)

4. **Check the log** - you should see:
   ```
   RocketBind: Plugin loaded successfully!
   RocketBind: Set window keybind to F6
   RocketBind: Press F6 to open menu OR use 'togglemenu rocketbind' console command
   ```

5. **Open the menu:**
   - **Press F6 key** (new keybind)
   - OR type in console: `togglemenu rocketbind`

6. **Verify status** with console command:
   ```
   rocketbind_status
   ```

## Why This is Different from F2 Menu

- **F2 Menu**: Opens BakkesMod's settings overlay (PluginSettingsWindow interface)
- **togglemenu + keybind**: Opens standalone plugin windows (PluginWindow interface)
- RocketPlugin uses PluginWindow, so we need the keybind approach

## Key Differences Between Our Plugin and RocketPlugin

| Feature | RocketPlugin | RocketBind (Fixed) |
|---------|-------------|-------------------|
| Interface | PluginWindow | PluginWindow |
| Default Keybind | Home | F6 |
| Menu Name | "rocketplugin" | "rocketbind" |
| Menu Title | "Rocket Plugin" | "RocketBind" |
| Keybind Check | ✅ Yes | ✅ Yes (NOW!) |
| Auto-bind on load | ✅ Yes | ✅ Yes (NOW!) |

## Technical Notes

- The `togglemenu` command is a BakkesMod built-in that toggles PluginWindow interfaces
- Without the keybind registration, the menu exists in memory but has no way to be accessed
- The binds.cfg file persists across sessions, so the keybind only needs to be set once
- Users can change the keybind using BakkesMod's keybind settings or by editing binds.cfg

## Build Output

```
RocketBind.vcxproj -> C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\RocketBind_BakkesMod\Release\RocketBind.dll
```

Build succeeded with no errors or warnings.

## Next Steps

1. Test in Rocket League
2. Verify menu opens with F6
3. Test all functionality (preset loading, saving, applying)
4. Consider adding a console command to set custom keybind
