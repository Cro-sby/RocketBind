# RocketBind Plugin - Testing Instructions

## ✅ Plugin Successfully Built!

Your RocketBind plugin has been compiled and is ready for testing in Rocket League.

## 📋 Installation Steps

1. **Locate the plugin DLL:**
   ```
   c:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\RocketBind_BakkesMod\Release\RocketBind.dll
   ```

2. **Copy to BakkesMod plugins folder:**
   - Default location: `%appdata%\bakkesmod\bakkesmod\plugins\`
   - Copy `RocketBind.dll` to this folder

3. **Launch Rocket League**

4. **Load the plugin:**
   - Open BakkesMod console (F6)
   - Type: `plugin load rocketbind`
   - You should see: `"RocketBind: Plugin loaded successfully!"`

## 🔍 Finding the Menu

### Method 1: F2 Menu (Primary Way)
1. Press **F2** while in Rocket League
2. Look for **"Plugins"** section in the menu
3. Find and click **"RocketBind"**
4. The menu window should open!

### Method 2: Console Commands (Debug/Status Only)
Open the BakkesMod console (F6) and try these commands:

- **`rocketbind_status`** - Shows plugin status (does NOT open menu - only F2 works!)
- **`rocketbind_refresh`** - Refreshes the preset list  
- **`rocketbind_info`** - Shows detailed plugin information

⚠️ **IMPORTANT:** Console commands cannot open the menu. You MUST use F2 to access the menu interface!

## 🐛 Troubleshooting

### Menu Not Appearing in F2?

1. **Check plugin is loaded:**
   ```
   plugin load rocketbind
   ```

2. **Run status command:**
   ```
   rocketbind_status
   ```
   
   This will show:
   - Plugin loaded status
   - Menu Name and Title
   - How to access the menu (F2)
   - Number of presets loaded

3. **Verify F2 menu access:**
   - Press F2 in-game
   - Look for "Plugins" tab
   - Find "RocketBind" entry
   - If it's there, the plugin is working!

4. **Check BakkesMod logs:**
   - Look in console (F6) for any error messages
   - Check if plugin loaded successfully

### Plugin Won't Load?

1. **Verify file location:**
   - Must be in: `%appdata%\bakkesmod\bakkesmod\plugins\`
   - File name must be: `RocketBind.dll`

2. **Check 64-bit:**
   - Plugin is compiled for 64-bit
   - Should work with modern BakkesMod/Rocket League

3. **Dependencies:**
   - Make sure BakkesMod is up to date
   - The plugin uses BakkesMod SDK features

## ✨ Expected Behavior

Once the menu opens, you should see:
- Orange header: "RocketBind - Keybinding Preset Manager"
- Section to **Load Existing Presets** (dropdown + Load button)
- Section to **Create New Preset** (text input + Save button)
- Section to **Delete Preset** (Delete button)
- Status messages and errors displayed inline

## 📁 Data Location

Presets are saved to:
```
%appdata%\bakkesmod\bakkesmod\data\RocketBind\
```

Each preset is a JSON file containing your controller bindings.

## 💡 Tips

- The menu is accessed via BakkesMod's F2 overlay system
- You can use console commands as an alternative
- Presets only save controller bindings (A, B, X, Y, triggers, etc.)
- Settings like sensitivity and camera are NOT affected

## 🎮 Usage Flow

1. **Save Current Bindings:**
   - Open menu (F2 -> Plugins -> RocketBind)
   - Enter a name (e.g., "Aerial Settings")
   - Click "Save Preset"

2. **Load Saved Bindings:**
   - Open menu
   - Select preset from dropdown
   - Click "Load Preset"
   - Bindings are instantly applied!

3. **Delete Old Presets:**
   - Select preset from dropdown
   - Click "Delete Preset"

---

## 🚀 Next Steps After Testing

If the menu appears and works:
- ✅ Test saving a preset
- ✅ Test loading a preset
- ✅ Test deleting a preset
- ✅ Verify bindings actually change in-game

If issues persist:
- Check the console (F6) for error messages
- Run `rocketbind_info` to debug
- Verify BakkesMod version is current
