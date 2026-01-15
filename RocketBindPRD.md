Here is the **Updated PRD**. I have stripped out all the logic regarding Sensitivity, Deadzone, and Camera settings.

This version strictly handles **Button-to-Action mappings** (Keybindings) only.

***

## **Project Title:** RocketBind (BakkesMod Plugin) - Lite

### **1. High-Level Overview**
**RocketBind** is a BakkesMod plugin for *Rocket League* that allows users to save and load **Keybinding configurations** instantly.
It strictly manages control schemes (e.g., swapping between "Freestyle" and "Competitive" button layouts) without altering sensitivities, camera settings, or deadzones.

### **2. Technical Stack**
*   **Language:** C++ (C++17 standard).
*   **SDK:** BakkesMod SDK.
*   **External Library:** `nlohmann/json` (single header) for parsing/saving data.
*   **UI Framework:** ImGui (Native BakkesMod wrapper).

### **3. Core Logic Requirements**

#### **A. The "Save Bindings" Logic (Pull)**
The plugin must iterate through a hardcoded list of supported Controller Inputs.
*   **Input List:** `XboxTypeS_A`, `XboxTypeS_B`, `XboxTypeS_X`, `XboxTypeS_Y`, `XboxTypeS_LeftShoulder`, `XboxTypeS_RightShoulder`, `XboxTypeS_LeftTrigger`, `XboxTypeS_RightTrigger`, `XboxTypeS_LeftThumbStick`, `XboxTypeS_RightThumbStick`, `XboxTypeS_Start`, `XboxTypeS_Back`, `XboxTypeS_DPad_Up`, `XboxTypeS_DPad_Down`, `XboxTypeS_DPad_Left`, `XboxTypeS_DPad_Right`.
*   **Action:** For each key, call `cvarManager->getBindString(key)`.
*   **Output:** Write this map to a JSON file at `bakkesmod/data/RocketBind/[PresetName].json`.
*   **Constraint:** Do **NOT** save sensitivity or deadzone values.

#### **B. The "Load Bindings" Logic (Push)**
The plugin must read a target `.json` file and apply the bindings immediately.
*   **Action:** Parse the JSON.
*   **Execution:** For every key/value pair in the JSON object, execute:
    `cvarManager->executeCommand("SetBind [Key] [Value]");`
*   **Toast:** Trigger a BakkesMod notification: `gameWrapper->Toast("RocketBind", "Keybindings Loaded!", ...)`

#### **C. Data Structure (JSON Schema)**
The generated files must follow this simplified format:
```json
{
  "bindings": {
    "XboxTypeS_A": "Jump",
    "XboxTypeS_B": "Boost",
    "XboxTypeS_X": "AirRollLeft",
    "XboxTypeS_RightTrigger": "Throttle"
  }
}
```

### **4. UI/UX Requirements (ImGui)**
The UI should be rendered via `RocketBind::Render()` inside the F2 Menu.
1.  **Preset Selector:** A `ImGui::Combo` (Dropdown) listing all `.json` files found in the data directory.
2.  **Action Buttons:**
    *   **"Load Keybindings":** triggers the Load logic.
    *   **"Refresh List":** Re-scans the directory.
3.  **Creation Section:**
    *   **Input Text:** `ImGui::InputText` for naming a new preset.
    *   **"Save Current Keybindings":** Button to trigger the Save logic.

### **5. File Structure & Implementation Plan**

Please generate the following files:

1.  **`RocketBind.h`**:
    *   Inherit from `BakkesMod::Plugin::BakkesModPlugin` and `BakkesMod::Plugin::PluginWindow`.
    *   Define the helper functions `SavePreset(std::string name)` and `LoadPreset(std::string name)`.
    *   Declare the `std::vector<std::string>` that holds the controller key names.

2.  **`RocketBind.cpp`**:
    *   Implementation of `onLoad` (ensure `data/RocketBind` folder exists).
    *   Implementation of the Save/Load logic using `nlohmann/json`.
    *   **Logic:** Iterate through the vector of keys. For Save: `getBindString`. For Load: `executeCommand("SetBind...")`.

3.  **`RocketBindGUI.cpp`**:
    *   Implementation of `Render()`.
    *   Logic to scan the directory `bakkesmod/data/RocketBind/` using `std::filesystem` to populate the dropdown.

### **6. Special Instructions for the AI**
*   **Error Handling:** Ensure the code checks if the directory exists before writing.
*   **Library:** Assume `json.hpp` is present in the include path.
*   **Scope:** Strictly limit logic to `SetBind` commands. Do not touch `GamepadSteeringSensitivity` or `Camera` CVars.

***

**How to use this:**
Copy/paste this into **Claude Sonnet**. It now knows to ignore sensitivities and focus only on the buttons.