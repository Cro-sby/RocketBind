Here is a complete, technically detailed **Product Requirement Document (PRD)** designed specifically to be pasted into **Claude**.

It covers the tech stack, the file logic, the validation rules (so users don’t break their controls), and the "Force Restart" automation.

***

## Project Title: RocketBind (RL Preset Manager)

### **1. High-Level Overview**
**RocketBind** is a native Windows desktop application that allows *Rocket League* players to create, save, and instantly swap between multiple controller/keyboard configurations (presets). Since the game does not support multiple control profiles natively, this app acts as a manager that overrides the game's configuration files and forces a game restart to apply changes immediately.

**Target Platform:** Windows 10/11 (Note: macOS support is unnecessary as Rocket League is no longer supported on macOS).

### **2. Tech Stack**
*   **Language:** Python (all logic, file handling, and UI will be implemented in Python).
*   **GUI Framework:** CustomTkinter (for a modern, dark-mode aesthetic similar to the Rocket League menu).
*   **File Handling:** Standard Python I/O for reading/writing `.ini` files.

### **3. Core MVP Features**

#### **A. Preset Management (The "Dashboard")**
*   **Create New Preset:** Start from scratch or duplicate an existing one.
*   **Import Current Settings:** A button that reads the user's currently active `TAInput.ini` file and saves it as a new preset in the app. *Technical Note: The `.ini` file is plain text, not encrypted, so parsing this is fully possible.*
*   **Edit Preset:** A visual interface to map actions (Jump, Boost, Air Roll) to buttons.
*   **Delete/Rename Presets.**

#### **B. The "Force Apply" System**
The app must execute the following "Macro" when the user clicks **APPLY PRESET**:
1.  **Check Process:** Check if `RocketLeague.exe` is running.
2.  **Kill Process:** If running, execute `taskkill /f /im RocketLeague.exe` to close it immediately.
3.  **File Swap:** Overwrite the contents of `%USERPROFILE%\Documents\My Games\Rocket League\TAGame\Config\TAInput.ini` with the data from the selected preset.
4.  **Auto-Relaunch:** Detect if the user uses Steam or Epic and launch the appropriate URI:
    *   **Steam:** `start steam://rungameid/252950`
    *   **Epic:** `start com.epicgames.launcher://apps/Sugar?action=launch&silent=true`

#### **C. Input Validation (The "Smart" Logic)**
To mimic Rocket League’s native menu and prevent broken controls, the app must include:
*   **Conflict Detection:** If a user binds "Jump" to `A` and then tries to bind "Boost" to `A`, the app should alert the user or unbind the previous action (optional toggle).
*   **Essential Check:** The user cannot save a preset unless critical actions (Throttle, Steer, Jump, Boost, Camera Swivel) are bound.
*   **Device Handling:** UI should distinguish between "Gamepad" (Xbox/PS bindings) and "PC" (Keyboard/Mouse bindings).

### **4. UI/UX Requirements**
*   **Visual Style:** Dark Blue/Grey background with Orange accents (Hex: `#0078F2` for Blue, `#FF8C00` for Orange).
*   **Layout:**
    *   **Left Sidebar:** List of Presets (e.g., "Freestyle", "Comp", "KBM").
    *   **Main Area:** Scrollable list of actions (Jump, Boost, Handbrake) with dropdown menus for the assigned key/button.
    *   **Bottom Bar:** Large "APPLY & RESTART" button (Red warning color if game is running).

### **5. Technical Specifications for the AI**

**File Paths:**
*   **Config Location:** `os.path.expanduser('~') + r"\Documents\My Games\Rocket League\TAGame\Config\TAInput.ini"`
*   **Backup:** The app must create a backup of the original `TAInput.ini` on first launch (`TAInput.ini.bak`) to prevent data loss.

**Parsing Logic (The tricky part):**
The `TAInput.ini` file uses Unreal Engine 3 syntax. The app needs to parse lines looking like:
`GamepadBindings=( Action="Jump", Key="XboxTypeS_A" )`
*   **Read Mode:** Regex parsing to extract the `Action` and the `Key`.
*   **Write Mode:** Reconstruct the file string preserving the header/footer structure of the original file, only modifying the `GamepadBindings` and `PCBindings` lines.

**Device Detection:**
*   Steam Version check: Registry lookup or checking if `steam_api64.dll` is loaded in the process (or just ask the user once on setup).

### **6. Edge Cases to Handle**
1.  **Read-Only Files:** If the user’s `TAInput.ini` is set to "Read Only" (common optimization in RL community), the app must remove that attribute before writing, then re-apply it if desired.
2.  **Cloud Save Conflict:** Sometimes Steam Cloud attempts to restore the old config. The app should advise the user to disable Steam Cloud for Rocket League if settings revert automatically.
3.  **Game Updates:** If Rocket League adds a new binding (e.g., a new rumble powerup), the app should not crash. It should treat unknown lines as "Pass-through" (keep them in the file, don't delete them).