#pragma once

#include "bakkesmod/plugin/bakkesmodplugin.h"
#include "bakkesmod/plugin/pluginwindow.h"
#include "json.hpp"  // nlohmann/json single header
#include <vector>
#include <string>

// Forward declare ImGui context
struct ImGuiContext;

using json = nlohmann::json;

/**
 * RocketBind - BakkesMod Plugin for Keybinding Preset Management
 * 
 * This plugin allows players to save and load controller keybinding
 * configurations instantly without modifying sensitivity or camera settings.
 */
class RocketBind : public BakkesMod::Plugin::BakkesModPlugin,
                   public BakkesMod::Plugin::PluginWindow
{
public:
    // Constructor
    RocketBind();

    // BakkesModPlugin overrides
    void onLoad() override;
    void onUnload() override;

    // PluginWindow overrides
    void Render() override;
    std::string GetMenuName() override;
    std::string GetMenuTitle() override;
    void SetImGuiContext(uintptr_t ctx) override;
    bool ShouldBlockInput() override;
    bool IsActiveOverlay() override;
    void OnOpen() override;
    void OnClose() override;

    // Core functionality
    void SavePreset(const std::string& name);
    void LoadPreset(const std::string& name);
    void RefreshPresetList();
    
    // GUI rendering
    void RenderGUI();

private:
    // State
    bool isOpen = false;
    // Hardcoded list of Xbox controller inputs to monitor
    std::vector<std::string> controllerKeys = {
        "XboxTypeS_A",
        "XboxTypeS_B",
        "XboxTypeS_X",
        "XboxTypeS_Y",
        "XboxTypeS_LeftShoulder",
        "XboxTypeS_RightShoulder",
        "XboxTypeS_LeftTrigger",
        "XboxTypeS_RightTrigger",
        "XboxTypeS_LeftThumbStick",
        "XboxTypeS_RightThumbStick",
        "XboxTypeS_Start",
        "XboxTypeS_Back",
        "XboxTypeS_DPad_Up",
        "XboxTypeS_DPad_Down",
        "XboxTypeS_DPad_Left",
        "XboxTypeS_DPad_Right"
    };

    // GUI state variables
    char newPresetNameBuffer[256] = "";
    std::vector<std::string> presetFiles;
    int selectedPresetIndex = 0;
    bool showError = false;
    std::string errorMessage = "";
};
