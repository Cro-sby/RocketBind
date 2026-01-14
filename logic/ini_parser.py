"""
INI Parser for Rocket League TAInput.ini files.
Handles reading and writing of GamepadBindings and PCBindings.
"""
import re
import os
from typing import Dict, List, Tuple


class IniParser:
    """Parse and manipulate Rocket League TAInput.ini files."""
    
    def __init__(self):
        self.header_lines = []
        self.footer_lines = []
        self.gamepad_bindings = []
        self.pc_bindings = []
        self.other_lines = []
        
    def parse_file(self, file_path: str) -> bool:
        """Parse an INI file and extract bindings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._parse_content(content)
            return True
        except Exception as e:
            print(f"Error parsing file: {e}")
            return False
    
    def _parse_content(self, content: str):
        """Parse the content of an INI file."""
        lines = content.split('\n')
        in_preset_section = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check if we're in the ControlPreset section
            if '[ProjectX.ControlPreset_X]' in line:
                in_preset_section = True
                self.header_lines.append(line)
                continue
            
            # Check if we're leaving the preset section
            if in_preset_section and stripped.startswith('[') and '[ProjectX.ControlPreset_X]' not in line:
                in_preset_section = False
            
            # Parse bindings
            if in_preset_section:
                if 'GamepadBindings=' in line:
                    binding = self._parse_binding_line(line, 'gamepad')
                    if binding:
                        self.gamepad_bindings.append(binding)
                elif 'PCBindings=' in line:
                    binding = self._parse_binding_line(line, 'pc')
                    if binding:
                        self.pc_bindings.append(binding)
                else:
                    self.other_lines.append(line)
            else:
                if not in_preset_section and not self.gamepad_bindings and not self.pc_bindings:
                    self.header_lines.append(line)
                elif self.gamepad_bindings or self.pc_bindings:
                    self.footer_lines.append(line)
    
    def _parse_binding_line(self, line: str, binding_type: str) -> Dict:
        """Parse a single binding line."""
        # Pattern: Action="Jump", Key="XboxTypeS_A"
        action_match = re.search(r'Action="([^"]+)"', line)
        key_match = re.search(r'Key="([^"]+)"', line)
        axis_match = re.search(r'AxisSign=AxisSign_(\w+)', line)
        press_match = re.search(r'PressType=BPT_(\w+)', line)
        speed_match = re.search(r'Speed=(\d+)', line)
        required_match = re.search(r'bRequired=(\w+)', line)
        remappable_match = re.search(r'Remappable=Remappable_(\w+)', line)
        
        if action_match:
            binding = {
                'type': binding_type,
                'action': action_match.group(1),
                'key': key_match.group(1) if key_match else '',
                'raw_line': line
            }
            
            # Add optional parameters
            if axis_match:
                binding['axis_sign'] = axis_match.group(1)
            if press_match:
                binding['press_type'] = press_match.group(1)
            if speed_match:
                binding['speed'] = speed_match.group(1)
            if required_match:
                binding['required'] = required_match.group(1) == 'true'
            if remappable_match:
                binding['remappable'] = remappable_match.group(1)
            
            return binding
        return None
    
    def write_file(self, file_path: str) -> bool:
        """Write the parsed data back to an INI file."""
        try:
            # Remove read-only attribute if present
            if os.path.exists(file_path):
                os.chmod(file_path, 0o666)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write header (everything before bindings)
                for line in self.header_lines:
                    f.write(line + '\n')
                
                # Write other lines in the preset section (like settings)
                for line in self.other_lines:
                    f.write(line + '\n')
                
                # Write PC bindings
                for binding in self.pc_bindings:
                    f.write(self._construct_binding_line(binding, 'PC') + '\n')
                
                # Write Gamepad bindings
                for binding in self.gamepad_bindings:
                    f.write(self._construct_binding_line(binding, 'Gamepad') + '\n')
                
                # Write footer (everything after bindings)
                for line in self.footer_lines:
                    f.write(line + '\n')
            
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def _construct_binding_line(self, binding: Dict, prefix: str) -> str:
        """Construct a binding line from a binding dictionary."""
        parts = [f'Action="{binding["action"]}"']
        
        if binding.get('key'):
            parts.append(f'Key="{binding["key"]}"')
        
        if binding.get('axis_sign'):
            parts.append(f'AxisSign=AxisSign_{binding["axis_sign"]}')
        
        if binding.get('press_type'):
            parts.append(f'PressType=BPT_{binding["press_type"]}')
        
        if binding.get('speed'):
            parts.append(f'Speed={binding["speed"]}')
        
        if binding.get('required'):
            parts.append('bRequired=true')
        
        if binding.get('remappable'):
            parts.append(f'Remappable=Remappable_{binding["remappable"]}')
        
        binding_str = ', '.join(parts)
        return f'{prefix}Bindings=( {binding_str} )'
    
    def get_binding(self, action: str, binding_type: str = 'both') -> Dict:
        """Get a specific binding by action name."""
        if binding_type in ['gamepad', 'both']:
            for binding in self.gamepad_bindings:
                if binding['action'] == action:
                    return binding
        
        if binding_type in ['pc', 'both']:
            for binding in self.pc_bindings:
                if binding['action'] == action:
                    return binding
        
        return None
    
    def set_binding(self, action: str, key: str, binding_type: str, **kwargs):
        """Set or update a binding."""
        bindings = self.gamepad_bindings if binding_type == 'gamepad' else self.pc_bindings
        
        # Check if binding exists
        for i, binding in enumerate(bindings):
            if binding['action'] == action:
                # Update existing binding
                bindings[i]['key'] = key
                for k, v in kwargs.items():
                    bindings[i][k] = v
                return
        
        # Create new binding
        new_binding = {
            'type': binding_type,
            'action': action,
            'key': key
        }
        new_binding.update(kwargs)
        bindings.append(new_binding)
    
    def get_all_bindings(self) -> Dict[str, List[Dict]]:
        """Get all bindings organized by type."""
        return {
            'gamepad': self.gamepad_bindings.copy(),
            'pc': self.pc_bindings.copy()
        }
