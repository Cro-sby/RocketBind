# RocketBind - Quick Build Guide

## Before You Start

1. ✅ CMake installed and working (`cmake --version`)
2. ✅ Visual Studio 2019/2022 with C++ tools
3. ✅ BakkesMod SDK at: `C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\BakkesModSDK-master`
4. ⚠️ **DOWNLOAD json.hpp** from: https://github.com/nlohmann/json/releases

## Step-by-Step Build

### 1. Download json.hpp
```
Go to: https://github.com/nlohmann/json/releases
Download: json.hpp (single header file)
Place in: RocketBind_BakkesMod/ folder (replace the placeholder)
```

### 2. Open Command Prompt
- Search for: "x64 Native Tools Command Prompt for VS 2022"
- Run as administrator (recommended)

### 3. Navigate to Plugin Folder
```cmd
cd "C:\Users\mmkk2\Desktop\VS Workspaces\RocketBind\RocketBind_BakkesMod"
```

### 4. Generate Build Files
```cmd
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
```

### 5. Compile
```cmd
cmake --build . --config Release
```

### 6. Install Plugin
```cmd
copy Release\RocketBind.dll "%APPDATA%\bakkesmod\bakkesmod\plugins\"
```

### 7. Load in Rocket League
- Launch Rocket League with BakkesMod
- Press F6 (console)
- Type: `plugin load RocketBind`
- Press F2 to open settings

## Common Issues

### "json.hpp not found"
- You forgot to download json.hpp
- Get it from: https://github.com/nlohmann/json/releases

### "pluginsdk.lib not found"
- Check SDK path in CMakeLists.txt
- Verify SDK folder structure

### "CMake not recognized"
- Restart terminal after installing CMake
- Add to PATH: `C:\Program Files\CMake\bin`

## Quick Rebuild After Changes

```cmd
cd build
cmake --build . --config Release
copy Release\RocketBind.dll "%APPDATA%\bakkesmod\bakkesmod\plugins\"
```

Then in Rocket League console (F6):
```
plugin unload RocketBind
plugin load RocketBind
```

---

**That's it! You're ready to build and use RocketBind!** 🚀
