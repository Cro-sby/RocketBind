# RocketBind - Quick Start Guide

## 🚀 Getting Started

### First Time Setup

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Import Your Current Settings**
   - Click the "Import" button in the sidebar
   - Enter a name (e.g., "My Current Settings")
   - This will import your existing Rocket League configuration

3. **Create Additional Presets**
   - Click "New" to create a fresh preset
   - Or click "Duplicate" to copy an existing one
   - Give it a meaningful name (e.g., "Freestyle", "Competitive", "KBM")

### Using Presets

1. **Viewing Bindings**
   - Click a preset name in the sidebar to view it
   - Switch between "Gamepad" and "Keyboard/Mouse" tabs
   - Bindings are organized by category (Driving, Actions, Aerial, Camera)

2. **Applying a Preset**
   - Select the preset you want to use
   - Choose your platform (Steam or Epic) at the bottom of the sidebar
   - Click the orange "APPLY & RESTART" button
   - The app will:
     - Close Rocket League if it's running
     - Apply your preset configuration
     - Relaunch the game automatically

### Tips

- **Always save changes** before applying if you've edited a preset
- **Create backups** by duplicating presets before making major changes
- **Check validation warnings** - the app will alert you about binding conflicts
- **Platform detection** - the app tries to auto-detect Steam/Epic, but you can change it manually

## 📁 Project Structure

```
RocketBind/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── logic/                 # Core business logic
│   ├── ini_parser.py      # TAInput.ini file parsing
│   ├── preset_manager.py  # Preset CRUD operations
│   └── validator.py       # Binding validation
├── ui/                    # User interface
│   └── main_window.py     # Main application window
├── utils/                 # Utilities
│   └── game_control.py    # Process control & game launching
└── presets/              # Stored presets (auto-created)
```

## 🔧 Technical Details

### What Gets Modified
- The app modifies: `%USERPROFILE%\Documents\My Games\Rocket League\TAGame\Config\TAInput.ini`
- A backup is automatically created as `TAInput.ini.bak` on first run
- Each preset is stored as a separate `.ini` file in the `presets/` folder

### Validation Rules
The app enforces these rules:
- Essential actions must be bound (Throttle, Steer, Jump, Boost, Handbrake)
- Warns about conflicting bindings (same key for incompatible actions)
- Compatible actions can share keys (e.g., Steer + Yaw, Throttle + Pitch)

### Platform Support
- **Steam**: Launches via `steam://rungameid/252950`
- **Epic**: Launches via `com.epicgames.launcher://apps/Sugar?action=launch&silent=true`

## 🐛 Troubleshooting

### "Failed to import"
- Check if Rocket League is installed
- Verify the config file exists at: `Documents\My Games\Rocket League\TAGame\Config\TAInput.ini`

### Settings revert after restart
- Disable Steam Cloud for Rocket League in Steam settings
- Make sure the config file isn't set to read-only manually elsewhere

### App won't close the game
- Make sure you're running the app with administrator privileges if needed
- Check Task Manager to ensure RocketLeague.exe fully closes

## 🎮 Common Use Cases

### Setup for Competitive Play
1. Import current settings as "Base Config"
2. Duplicate it and name "Competitive"
3. Edit to optimize for competitive play
4. Apply when playing ranked

### Setup for Freestyle
1. Create new preset "Freestyle"
2. Assign air roll left/right to bumpers
3. Adjust camera settings if needed
4. Apply when practicing in freeplay

### Multiple Input Methods
1. Create "Controller Main" preset
2. Create "Keyboard Backup" preset
3. Switch between them based on what you're using

## 💡 Future Enhancements

Potential features for future versions:
- Full key rebinding UI with key capture
- Preset sharing/export
- Cloud sync between computers
- Advanced binding macros
- Integration with BakkesMod
- Support for custom training pack presets

## ⚡ Performance Notes

- Preset switching is instant (file operations take <100ms)
- Game restart typically takes 15-30 seconds depending on your system
- No performance impact while gaming (app doesn't run in background)

## 📝 Contributing

This is an open-source project. Contributions welcome:
- Bug reports and feature requests
- Code improvements and optimizations
- UI/UX enhancements
- Documentation improvements

---

**Enjoy your enhanced Rocket League experience! 🚗💨⚽**
