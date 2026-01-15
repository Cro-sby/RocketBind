#include "RocketBind.h"
#include "imgui.h"

void RocketBind::RenderGUI()
{
    ImGui::TextColored(ImVec4(1.0f, 0.5f, 0.0f, 1.0f), "RocketBind - Keybinding Preset Manager");
    ImGui::Separator();
    ImGui::Spacing();

    // Display error message if any
    if (showError)
    {
        ImGui::PushStyleColor(ImGuiCol_Text, ImVec4(1.0f, 0.2f, 0.2f, 1.0f));
        ImGui::TextWrapped("%s", errorMessage.c_str());
        ImGui::PopStyleColor();
        
        if (ImGui::Button("Dismiss"))
        {
            showError = false;
            errorMessage = "";
        }
        ImGui::Separator();
        ImGui::Spacing();
    }

    // Section 1: Load Preset
    ImGui::Text("Load Existing Preset");
    ImGui::Spacing();

    if (presetFiles.empty())
    {
        ImGui::TextColored(ImVec4(0.7f, 0.7f, 0.7f, 1.0f), "No presets found. Create one below!");
    }
    else
    {
        // Preset dropdown
        if (ImGui::BeginCombo("##PresetSelector", 
            selectedPresetIndex < presetFiles.size() 
                ? presetFiles[selectedPresetIndex].c_str() 
                : "Select a preset..."))
        {
            for (int i = 0; i < presetFiles.size(); i++)
            {
                bool isSelected = (selectedPresetIndex == i);
                if (ImGui::Selectable(presetFiles[i].c_str(), isSelected))
                {
                    selectedPresetIndex = i;
                }
                if (isSelected)
                {
                    ImGui::SetItemDefaultFocus();
                }
            }
            ImGui::EndCombo();
        }

        ImGui::Spacing();

        // Load button
        if (ImGui::Button("Load Keybindings", ImVec2(200, 30)))
        {
            if (selectedPresetIndex >= 0 && selectedPresetIndex < presetFiles.size())
            {
                std::string presetToLoad = presetFiles[selectedPresetIndex];
                // Execute in game thread to avoid crashes
                gameWrapper->Execute([this, presetToLoad](GameWrapper* gw) {
                    LoadPreset(presetToLoad);
                });
            }
        }

        ImGui::SameLine();

        // Refresh button
        if (ImGui::Button("Refresh List", ImVec2(150, 30)))
        {
            // Execute in game thread to avoid crashes
            gameWrapper->Execute([this](GameWrapper* gw) {
                RefreshPresetList();
            });
        }
    }

    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();

    // Section 2: Save New Preset
    ImGui::Text("Save Current Keybindings");
    ImGui::Spacing();

    ImGui::InputText("Preset Name", newPresetNameBuffer, sizeof(newPresetNameBuffer));
    
    ImGui::Spacing();

    if (ImGui::Button("Save Current Keybindings", ImVec2(200, 30)))
    {
        std::string presetName(newPresetNameBuffer);
        if (!presetName.empty())
        {
            // Execute in game thread to avoid crashes
            gameWrapper->Execute([this, presetName](GameWrapper* gw) {
                SavePreset(presetName);
            });
        }
        else
        {
            errorMessage = "Please enter a preset name!";
            showError = true;
        }
    }

    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();

    // Info section
    ImGui::TextColored(ImVec4(0.5f, 0.8f, 1.0f, 1.0f), "How to use:");
    ImGui::BulletText("Save your current keybindings as a preset");
    ImGui::BulletText("Load any saved preset instantly");
    ImGui::BulletText("Presets are saved in: bakkesmod/data/RocketBind/");
    
    ImGui::Spacing();
    ImGui::Text("Total Presets: %d", static_cast<int>(presetFiles.size()));
}
