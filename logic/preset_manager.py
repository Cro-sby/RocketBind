"""
Preset Manager for RocketBind.
Handles creating, loading, saving, and managing presets.
"""
import os
import shutil
from typing import List, Dict
from logic.ini_parser import IniParser


class PresetManager:
    """Manage Rocket League control presets."""
    
    def __init__(self, presets_dir: str):
        self.presets_dir = presets_dir
        self.current_preset = None
        
        # Ensure presets directory exists
        os.makedirs(presets_dir, exist_ok=True)
    
    def get_preset_list(self) -> List[str]:
        """Get list of all saved presets."""
        try:
            files = os.listdir(self.presets_dir)
            presets = [f[:-4] for f in files if f.endswith('.ini')]
            return sorted(presets)
        except Exception as e:
            print(f"Error listing presets: {e}")
            return []
    
    def load_preset(self, preset_name: str) -> IniParser:
        """Load a preset by name."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
        
        if not os.path.exists(preset_path):
            return None
        
        parser = IniParser()
        if parser.parse_file(preset_path):
            self.current_preset = preset_name
            return parser
        return None
    
    def save_preset(self, preset_name: str, parser: IniParser) -> bool:
        """Save a preset."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
        
        try:
            if parser.write_file(preset_path):
                self.current_preset = preset_name
                return True
        except Exception as e:
            print(f"Error saving preset: {e}")
        return False
    
    def create_preset(self, preset_name: str, source_parser: IniParser = None) -> bool:
        """Create a new preset."""
        if not preset_name:
            return False
        
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
        
        # Check if preset already exists
        if os.path.exists(preset_path):
            return False
        
        # If no source parser, create empty preset with default structure
        if source_parser is None:
            source_parser = self._create_default_parser()
        
        return self.save_preset(preset_name, source_parser)
    
    def duplicate_preset(self, source_name: str, new_name: str) -> bool:
        """Duplicate an existing preset."""
        source_path = os.path.join(self.presets_dir, f"{source_name}.ini")
        new_path = os.path.join(self.presets_dir, f"{new_name}.ini")
        
        if not os.path.exists(source_path) or os.path.exists(new_path):
            return False
        
        try:
            shutil.copy2(source_path, new_path)
            return True
        except Exception as e:
            print(f"Error duplicating preset: {e}")
            return False
    
    def rename_preset(self, old_name: str, new_name: str) -> bool:
        """Rename a preset."""
        old_path = os.path.join(self.presets_dir, f"{old_name}.ini")
        new_path = os.path.join(self.presets_dir, f"{new_name}.ini")
        
        if not os.path.exists(old_path) or os.path.exists(new_path):
            return False
        
        try:
            os.rename(old_path, new_path)
            if self.current_preset == old_name:
                self.current_preset = new_name
            return True
        except Exception as e:
            print(f"Error renaming preset: {e}")
            return False
    
    def delete_preset(self, preset_name: str) -> bool:
        """Delete a preset."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
        
        if not os.path.exists(preset_path):
            return False
        
        try:
            os.remove(preset_path)
            if self.current_preset == preset_name:
                self.current_preset = None
            return True
        except Exception as e:
            print(f"Error deleting preset: {e}")
            return False
    
    def import_from_game(self, game_config_path: str, preset_name: str) -> bool:
        """Import current settings from the game's TAInput.ini."""
        if not os.path.exists(game_config_path):
            return False
        
        parser = IniParser()
        if parser.parse_file(game_config_path):
            return self.save_preset(preset_name, parser)
        return False
    
    def _create_default_parser(self) -> IniParser:
        """Create a parser with default bindings."""
        parser = IniParser()
        
        # Add essential default bindings
        default_gamepad = [
            {'type': 'gamepad', 'action': 'ThrottleForward', 'key': 'XboxTypeS_RightTriggerAxis', 'axis_sign': 'Positive', 'required': True},
            {'type': 'gamepad', 'action': 'ThrottleReverse', 'key': 'XboxTypeS_LeftTriggerAxis', 'axis_sign': 'Positive', 'required': True},
            {'type': 'gamepad', 'action': 'SteerRight', 'key': 'XboxTypeS_LeftX', 'axis_sign': 'Positive'},
            {'type': 'gamepad', 'action': 'SteerLeft', 'key': 'XboxTypeS_LeftX', 'axis_sign': 'Negative'},
            {'type': 'gamepad', 'action': 'Jump', 'key': 'XboxTypeS_A', 'required': True},
            {'type': 'gamepad', 'action': 'Boost', 'key': 'XboxTypeS_B', 'required': True},
            {'type': 'gamepad', 'action': 'Handbrake', 'key': 'XboxTypeS_X', 'required': True},
            {'type': 'gamepad', 'action': 'SecondaryCamera', 'key': 'XboxTypeS_Y'},
        ]
        
        default_pc = [
            {'type': 'pc', 'action': 'ThrottleForward', 'key': 'W'},
            {'type': 'pc', 'action': 'ThrottleReverse', 'key': 'S'},
            {'type': 'pc', 'action': 'SteerRight', 'key': 'D'},
            {'type': 'pc', 'action': 'SteerLeft', 'key': 'A'},
            {'type': 'pc', 'action': 'Jump', 'key': 'RightMouseButton'},
            {'type': 'pc', 'action': 'Boost', 'key': 'LeftMouseButton'},
            {'type': 'pc', 'action': 'Handbrake', 'key': 'LeftShift'},
        ]
        
        parser.gamepad_bindings = default_gamepad
        parser.pc_bindings = default_pc
        parser.header_lines = ['[ProjectX.ControlPreset_X]']
        
        return parser
