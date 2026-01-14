# RocketBind Development Guide

## 🏗️ Architecture Overview

RocketBind follows a clean, modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│              main.py (Entry)                │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         ui/main_window.py (UI Layer)        │
│  - User interactions                        │
│  - Event handling                           │
│  - Display logic                            │
└────┬──────────┬─────────────┬───────────────┘
     │          │             │
     ▼          ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────────┐
│ logic/  │ │ utils/   │ │ presets/     │
│ (Core)  │ │ (Helper) │ │ (Storage)    │
└─────────┘ └──────────┘ └──────────────┘
```

## 📁 Module Responsibilities

### main.py
- Application entry point
- Minimal logic - just launches UI
- Good place for global exception handling

### ui/main_window.py
- All UI components and layout
- Event handlers for user actions
- Coordinates between logic modules
- No business logic - delegates to logic layer

### logic/ini_parser.py
- **Purpose**: Parse and write TAInput.ini files
- **Key Methods**:
  - `parse_file()` - Read and parse INI file
  - `write_file()` - Write bindings back to file
  - `get_binding()` - Retrieve specific binding
  - `set_binding()` - Update or create binding
- **Design**: Preserves unknown lines for forward compatibility

### logic/preset_manager.py
- **Purpose**: Manage preset files (CRUD operations)
- **Key Methods**:
  - `load_preset()` - Load preset from disk
  - `save_preset()` - Save preset to disk
  - `create_preset()` - Create new preset
  - `duplicate_preset()` - Copy existing preset
  - `delete_preset()` - Remove preset
  - `import_from_game()` - Import from RL config
- **Design**: File-based storage in presets/ directory

### logic/validator.py
- **Purpose**: Validate bindings for conflicts and completeness
- **Key Methods**:
  - `validate_bindings()` - Full validation check
  - `check_single_binding()` - Validate one binding
- **Design**: Rule-based validation with extensible rules

### utils/game_control.py
- **Purpose**: Process management and game launching
- **Key Classes**:
  - `GameController` - Kill/launch game
  - `ConfigBackup` - Backup management
- **Design**: Uses psutil for reliable process control

## 🔧 How to Add Features

### Adding a New Binding Action

1. **Define the action** in the validator's action lists:
```python
# logic/validator.py
ESSENTIAL_ACTIONS = [
    'ThrottleForward',
    'YourNewAction',  # Add here
    # ...
]
```

2. **Add to UI categorization**:
```python
# ui/main_window.py, in _display_binding_list()
action_actions = ['Jump', 'Boost', 'YourNewAction']
```

3. **Test** with a preset that includes the new action

### Adding Key Rebinding Dialog

Here's the skeleton for implementing key capture:

```python
# ui/key_capture_dialog.py
import customtkinter as ctk

class KeyCaptureDialog(ctk.CTkToplevel):
    def __init__(self, parent, action_name, current_key):
        super().__init__(parent)
        self.title(f"Rebind {action_name}")
        self.geometry("400x200")
        
        self.captured_key = None
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=f"Press a key to bind to {action_name}",
            font=ctk.CTkFont(size=14)
        )
        self.label.pack(pady=20)
        
        # Current key display
        self.current = ctk.CTkLabel(
            self,
            text=f"Current: {current_key}",
            text_color="#888888"
        )
        self.current.pack(pady=10)
        
        # Bind key press
        self.bind("<Key>", self.on_key_press)
        self.focus()
        
    def on_key_press(self, event):
        self.captured_key = event.keysym
        self.label.configure(text=f"Captured: {self.captured_key}")
        # Close after short delay
        self.after(500, self.destroy)
    
    def get_key(self):
        self.wait_window()
        return self.captured_key
```

Then in main_window.py:
```python
def _edit_binding(self, binding: Dict, binding_type: str):
    from ui.key_capture_dialog import KeyCaptureDialog
    
    dialog = KeyCaptureDialog(
        self, 
        binding['action'], 
        binding.get('key', 'Unbound')
    )
    new_key = dialog.get_key()
    
    if new_key:
        # Validate
        bindings = (self.current_parser.gamepad_bindings 
                   if binding_type == 'gamepad' 
                   else self.current_parser.pc_bindings)
        
        is_valid, error = self.validator.check_single_binding(
            binding['action'], 
            new_key, 
            bindings
        )
        
        if not is_valid:
            self._set_status(error, error=True)
            return
        
        # Update binding
        self.current_parser.set_binding(
            binding['action'],
            new_key,
            binding_type
        )
        
        # Refresh display
        self._display_bindings()
        self._set_status(f"Updated {binding['action']} to {new_key}")
```

### Adding Preset Export/Import

1. **Add to preset_manager.py**:
```python
def export_preset(self, preset_name: str, export_path: str) -> bool:
    """Export preset to a file."""
    preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
    if not os.path.exists(preset_path):
        return False
    
    try:
        shutil.copy2(preset_path, export_path)
        return True
    except Exception as e:
        print(f"Error exporting: {e}")
        return False

def import_preset_file(self, import_path: str, preset_name: str) -> bool:
    """Import preset from a file."""
    preset_path = os.path.join(self.presets_dir, f"{preset_name}.ini")
    if os.path.exists(preset_path):
        return False  # Preset name already exists
    
    try:
        shutil.copy2(import_path, preset_path)
        return True
    except Exception as e:
        print(f"Error importing: {e}")
        return False
```

2. **Add UI buttons** in main_window.py sidebar

### Adding Undo/Redo

1. **Add to preset_manager.py**:
```python
class PresetManager:
    def __init__(self, presets_dir: str):
        # ... existing code ...
        self.undo_stack = []
        self.redo_stack = []
    
    def push_undo(self, parser: IniParser):
        """Save current state for undo."""
        import copy
        self.undo_stack.append(copy.deepcopy(parser))
        self.redo_stack.clear()  # Clear redo on new action
    
    def undo(self) -> Optional[IniParser]:
        """Undo last change."""
        if not self.undo_stack:
            return None
        self.redo_stack.append(self.current_parser)
        return self.undo_stack.pop()
    
    def redo(self) -> Optional[IniParser]:
        """Redo last undone change."""
        if not self.redo_stack:
            return None
        self.undo_stack.append(self.current_parser)
        return self.redo_stack.pop()
```

2. **Add keyboard shortcuts** in main_window.py:
```python
def __init__(self):
    # ... existing code ...
    self.bind("<Control-z>", lambda e: self._undo())
    self.bind("<Control-y>", lambda e: self._redo())
```

## 🧪 Testing Strategy

### Unit Tests
Create `tests/` directory with:

```python
# tests/test_ini_parser.py
import unittest
from logic.ini_parser import IniParser

class TestIniParser(unittest.TestCase):
    def test_parse_binding_line(self):
        parser = IniParser()
        line = 'GamepadBindings=( Action="Jump", Key="XboxTypeS_A" )'
        binding = parser._parse_binding_line(line, 'gamepad')
        
        self.assertEqual(binding['action'], 'Jump')
        self.assertEqual(binding['key'], 'XboxTypeS_A')
    
    def test_construct_binding_line(self):
        parser = IniParser()
        binding = {
            'action': 'Jump',
            'key': 'XboxTypeS_A',
            'required': True
        }
        line = parser._construct_binding_line(binding, 'Gamepad')
        
        self.assertIn('Action="Jump"', line)
        self.assertIn('Key="XboxTypeS_A"', line)
        self.assertIn('bRequired=true', line)

# Run: python -m unittest discover tests
```

### Integration Tests
```python
# tests/test_integration.py
def test_full_workflow():
    # Create manager
    manager = PresetManager('test_presets')
    
    # Create preset
    assert manager.create_preset('test')
    
    # Load preset
    parser = manager.load_preset('test')
    assert parser is not None
    
    # Modify
    parser.set_binding('Jump', 'Space', 'pc')
    
    # Save
    assert manager.save_preset('test', parser)
    
    # Verify
    parser2 = manager.load_preset('test')
    binding = parser2.get_binding('Jump', 'pc')
    assert binding['key'] == 'Space'
```

## 🐛 Debugging Tips

### Common Issues

1. **Bindings not applying**
   - Check if game is actually closed
   - Verify TAInput.ini path is correct
   - Check file permissions

2. **Parse errors**
   - Add debug prints in `_parse_binding_line()`
   - Check for unexpected INI format
   - Verify regex patterns match actual data

3. **UI not updating**
   - Call `self.update()` after state changes
   - Check if event handlers are bound correctly
   - Verify data is actually changing in backend

### Debug Mode
Add to main.py:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Then use in modules:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug(f"Parsing binding: {line}")
logger.info(f"Preset loaded: {preset_name}")
logger.error(f"Failed to write file: {e}")
```

## 📊 Performance Optimization

### Current Performance
- Preset load: <50ms ✅
- File write: <100ms ✅
- UI render: <200ms ✅

### If You Need to Optimize

1. **Lazy Loading**: Don't parse all presets on startup
2. **Caching**: Cache parsed presets in memory
3. **Async Operations**: Use threading for file I/O
4. **Virtual Scrolling**: For very long binding lists

Example async save:
```python
import threading

def _save_changes_async(self):
    def save_thread():
        success = self.preset_manager.save_preset(
            self.selected_preset, 
            self.current_parser
        )
        # Update UI on main thread
        self.after(0, lambda: self._on_save_complete(success))
    
    threading.Thread(target=save_thread, daemon=True).start()
```

## 🎨 Styling Guide

### Color Palette
```python
COLOR_BG = "#1a1a2e"        # Dark blue background
COLOR_SIDEBAR = "#16213e"    # Darker sidebar
COLOR_ACCENT = "#FF8C00"     # Orange accent (Rocket League)
COLOR_BLUE = "#0078F2"       # Blue accent
COLOR_WARNING = "#FF4444"    # Red warning
```

### Font Standards
```python
FONT_TITLE = ctk.CTkFont(size=24, weight="bold")
FONT_HEADER = ctk.CTkFont(size=20, weight="bold")
FONT_SUBHEADER = ctk.CTkFont(size=14, weight="bold")
FONT_NORMAL = ctk.CTkFont(size=12)
FONT_SMALL = ctk.CTkFont(size=10)
```

### Widget Sizing
- Buttons: height=35-40px, width=100-200px
- Labels: height=25-30px
- Frames: padding=10-20px
- Gaps: 5-10px between related, 15-20px between sections

## 📝 Code Style

Follow PEP 8 with these additions:

1. **Docstrings**: All public methods
2. **Type hints**: Where it adds clarity
3. **Comments**: For complex logic only
4. **Line length**: 100 characters max
5. **Imports**: Grouped (stdlib, third-party, local)

Example:
```python
from typing import Dict, List, Optional
import os

from logic.ini_parser import IniParser
from utils.game_control import GameController


class PresetManager:
    """
    Manage Rocket League control presets.
    
    Handles CRUD operations for preset files stored in the
    presets directory. Each preset is a separate .ini file.
    """
    
    def load_preset(self, preset_name: str) -> Optional[IniParser]:
        """
        Load a preset by name.
        
        Args:
            preset_name: Name of preset without .ini extension
            
        Returns:
            IniParser instance if successful, None otherwise
        """
        # Implementation...
```

## 🚀 Deployment

### Building Executable (PyInstaller)

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create spec file:
```bash
pyinstaller --name="RocketBind" --windowed --onefile main.py
```

3. Customize `RocketBind.spec`:
```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('presets', 'presets')],  # Include presets dir
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
```

4. Build:
```bash
pyinstaller RocketBind.spec
```

### Distribution
- Executable in `dist/RocketBind.exe`
- Include README.md
- Include example preset (optional)
- Create installer with NSIS or Inno Setup

## 🔐 Security Considerations

1. **File Permissions**: Always check before writing
2. **Path Validation**: Sanitize user-provided paths
3. **Process Safety**: Verify process before killing
4. **Backup**: Always backup before modifying
5. **Error Messages**: Don't expose sensitive paths

## 📚 Resources

- CustomTkinter Docs: https://github.com/TomSchimansky/CustomTkinter
- psutil Docs: https://psutil.readthedocs.io/
- Python Regex: https://docs.python.org/3/library/re.html
- Rocket League Config Format: (reverse-engineered)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

### PR Checklist
- [ ] Code follows style guide
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Tested on Windows 10/11
- [ ] No breaking changes (or documented)

---

**Happy Coding! 🚗💨**
