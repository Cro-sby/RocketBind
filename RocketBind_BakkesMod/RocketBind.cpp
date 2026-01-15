#include "RocketBind.h"
#include "imgui.h"
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

// Macro for BakkesMod plugin export
BAKKESMOD_PLUGIN(RocketBind, "RocketBind", "1.0", 0)

// Default keybind for the GUI (can be changed by user)
constexpr const char* DEFAULT_GUI_KEYBIND = "Home";

RocketBind::RocketBind() {}

/// <summary>Checks if the GUI window is bound to a key.</summary>
/// <param name="windowName">Name of the GUI window</param>
/// <returns>Bool with if the GUI window is bound</returns>
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

void RocketBind::onLoad()
{
    // Validate pointers
    if (!gameWrapper || !cvarManager)
    {
        return;
    }

    // Get BakkesMod directories
    fs::path bakkesModFolder = gameWrapper->GetBakkesModPath();
    fs::path bindsFilePath = bakkesModFolder / "cfg" / "binds.cfg";
    fs::path dataDir = gameWrapper->GetDataFolder() / "RocketBind";
    
    // Create data directory if it doesn't exist
    if (!fs::exists(dataDir))
    {
        try 
        {
            fs::create_directories(dataDir);
            cvarManager->log("RocketBind: Created data directory at " + dataDir.string());
        }
        catch (const std::exception& e)
        {
            cvarManager->log("RocketBind: ERROR creating directory: " + std::string(e.what()));
            return;
        }
    }

    // Set the window bind to the default keybind if it is not set
    if (!IsGUIWindowBound(GetMenuName(), bindsFilePath))
    {
        cvarManager->setBind(DEFAULT_GUI_KEYBIND, "togglemenu " + GetMenuName());
        cvarManager->log("RocketBind: Set window keybind to " + std::string(DEFAULT_GUI_KEYBIND));
    }

    // Refresh the preset list on startup
    RefreshPresetList();

    // Register console commands for debugging
    cvarManager->registerNotifier("rocketbind_status", [this](std::vector<std::string> params) {
        cvarManager->log("=== RocketBind Status ===");
        cvarManager->log("Plugin is loaded and ready!");
        cvarManager->log("Plugin Name: RocketBind");
        cvarManager->log("Menu can be opened with: Home key OR 'togglemenu rocketbind' command");
        cvarManager->log("Presets loaded: " + std::to_string(presetFiles.size()));
    }, "Shows RocketBind status (does NOT open menu)", PERMISSION_ALL);

    cvarManager->registerNotifier("rocketbind_refresh", [this](std::vector<std::string> params) {
        RefreshPresetList();
        cvarManager->log("RocketBind: Refreshed preset list. Found " + std::to_string(presetFiles.size()) + " presets.");
    }, "Refreshes the preset list", PERMISSION_ALL);

    cvarManager->registerNotifier("rocketbind_info", [this, dataDir](std::vector<std::string> params) {
        cvarManager->log("=== RocketBind Plugin Info ===");
        cvarManager->log("Plugin Name: RocketBind");
        cvarManager->log("Presets Found: " + std::to_string(presetFiles.size()));
        cvarManager->log("Data Directory: " + dataDir.string());
        cvarManager->log("=== Press Home key in-game to open RocketBind menu ===");
        cvarManager->log("=== Or use console command: togglemenu rocketbind ===");
    }, "Shows RocketBind plugin information", PERMISSION_ALL);

    cvarManager->log("RocketBind: Plugin loaded successfully!");
    cvarManager->log("RocketBind: Press Home key to open menu OR use 'togglemenu rocketbind' console command");
    cvarManager->log("RocketBind: Use 'rocketbind_info' command for more information");
}

void RocketBind::onUnload()
{
    cvarManager->log("RocketBind: Plugin unloaded.");
}

void RocketBind::SavePreset(const std::string& name)
{
    if (!gameWrapper || !cvarManager)
    {
        errorMessage = "Plugin not initialized!";
        showError = true;
        return;
    }

    if (name.empty())
    {
        errorMessage = "Preset name cannot be empty!";
        showError = true;
        return;
    }

    // Get data directory
    fs::path dataDir = fs::path(gameWrapper->GetDataFolder()) / "RocketBind";
    
    // Ensure directory exists
    if (!fs::exists(dataDir))
    {
        try 
        {
            fs::create_directories(dataDir);
        }
        catch (const std::exception& e)
        {
            errorMessage = "Failed to create directory: " + std::string(e.what());
            showError = true;
            cvarManager->log("RocketBind: " + errorMessage);
            return;
        }
    }

    // Build JSON object with current bindings
    json j;
    for (const auto& key : controllerKeys)
    {
        std::string action = cvarManager->getBindStringForKey(key);
        j["bindings"][key] = action;
    }

    // Write to file
    fs::path filePath = dataDir / (name + ".json");
    std::ofstream out(filePath);
    
    if (out.is_open())
    {
        out << j.dump(4);  // Pretty print with 4 space indent
        out.close();
        
        cvarManager->log("RocketBind: Preset saved successfully: " + filePath.string());
        gameWrapper->Toast("RocketBind", "Preset Saved!", "Saved as: " + name, 3.0f, ToastType_OK);
        
        // Refresh list to show new preset
        RefreshPresetList();
        
        // Clear input field
        newPresetNameBuffer[0] = '\0';
    }
    else
    {
        errorMessage = "Failed to write preset file: " + filePath.string();
        showError = true;
        cvarManager->log("RocketBind: " + errorMessage);
    }
}

void RocketBind::LoadPreset(const std::string& name)
{
    if (!gameWrapper || !cvarManager)
    {
        errorMessage = "Plugin not initialized!";
        showError = true;
        return;
    }

    if (name.empty())
    {
        errorMessage = "No preset selected!";
        showError = true;
        return;
    }

    // Get full file path
    fs::path dataDir = fs::path(gameWrapper->GetDataFolder()) / "RocketBind";
    fs::path filePath = dataDir / name;

    // Check if file exists
    if (!fs::exists(filePath))
    {
        errorMessage = "Preset file not found: " + name;
        showError = true;
        cvarManager->log("RocketBind: " + errorMessage);
        return;
    }

    // Read JSON file
    std::ifstream in(filePath);
    if (!in.is_open())
    {
        errorMessage = "Failed to open preset file: " + name;
        showError = true;
        cvarManager->log("RocketBind: " + errorMessage);
        return;
    }

    // Parse JSON
    json j;
    try 
    {
        in >> j;
        in.close();
    }
    catch (const std::exception& e)
    {
        errorMessage = "Failed to parse JSON: " + std::string(e.what());
        showError = true;
        cvarManager->log("RocketBind: " + errorMessage);
        return;
    }

    // Validate JSON structure
    if (!j.contains("bindings") || !j["bindings"].is_object())
    {
        errorMessage = "Invalid preset format: missing 'bindings' object";
        showError = true;
        cvarManager->log("RocketBind: " + errorMessage);
        return;
    }

    // Apply all bindings
    int bindingsApplied = 0;
    for (auto& [key, value] : j["bindings"].items())
    {
        if (value.is_string())
        {
            std::string action = value.get<std::string>();
            std::string cmd = "SetBind " + key + " " + action;
            cvarManager->executeCommand(cmd);
            bindingsApplied++;
        }
    }

    // Show success notification
    cvarManager->log("RocketBind: Loaded preset '" + name + "' (" + 
                     std::to_string(bindingsApplied) + " bindings applied)");
    gameWrapper->Toast("RocketBind", "Keybindings Loaded!", 
                      "Preset: " + name.substr(0, name.find_last_of('.')), 
                      3.0f, ToastType_OK);
}

void RocketBind::RefreshPresetList()
{
    if (!gameWrapper)
    {
        return;
    }

    presetFiles.clear();
    
    fs::path dataDir = fs::path(gameWrapper->GetDataFolder()) / "RocketBind";
    
    if (!fs::exists(dataDir))
    {
        cvarManager->log("RocketBind: Data directory doesn't exist yet");
        return;
    }

    try 
    {
        for (const auto& entry : fs::directory_iterator(dataDir))
        {
            if (entry.is_regular_file() && entry.path().extension() == ".json")
            {
                presetFiles.push_back(entry.path().filename().string());
            }
        }
    }
    catch (const std::exception& e)
    {
        cvarManager->log("RocketBind: ERROR scanning directory: " + std::string(e.what()));
    }

    // Reset selection if out of bounds
    if (selectedPresetIndex >= static_cast<int>(presetFiles.size()))
    {
        selectedPresetIndex = 0;
    }

    cvarManager->log("RocketBind: Found " + std::to_string(presetFiles.size()) + " preset(s)");
}

// ========================================
// PluginWindow Implementation
// ========================================

std::string RocketBind::GetMenuName()
{
    return "rocketbind";
}

std::string RocketBind::GetMenuTitle()
{
    return "RocketBind";
}

void RocketBind::SetImGuiContext(uintptr_t ctx)
{
    ImGui::SetCurrentContext(reinterpret_cast<ImGuiContext*>(ctx));
}

bool RocketBind::ShouldBlockInput()
{
    return ImGui::GetIO().WantCaptureMouse || ImGui::GetIO().WantCaptureKeyboard;
}

bool RocketBind::IsActiveOverlay()
{
    return false;
}

void RocketBind::OnOpen()
{
    isOpen = true;
}

void RocketBind::OnClose()
{
    isOpen = false;
}

void RocketBind::Render()
{
    // Call the GUI rendering
    RenderGUI();
}
