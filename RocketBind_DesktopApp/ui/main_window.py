"""
Main application window for RocketBind.
"""
import customtkinter as ctk
import os
from typing import Dict, List
from logic.ini_parser import IniParser
from logic.preset_manager import PresetManager
from logic.validator import BindingValidator
from utils.game_control import GameController, ConfigBackup


# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RocketBindApp(ctk.CTk):
    """Main application window."""
    
    # Color scheme
    COLOR_BG = "#1a1a2e"
    COLOR_SIDEBAR = "#16213e"
    COLOR_ACCENT = "#FF8C00"
    COLOR_BLUE = "#0078F2"
    COLOR_WARNING = "#FF4444"
    
    # Game config path
    GAME_CONFIG_PATH = os.path.expanduser(
        r'~\Documents\My Games\Rocket League\TAGame\Config\TAInput.ini'
    )
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("RocketBind - Rocket League Preset Manager")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Initialize managers
        presets_dir = os.path.join(os.path.dirname(__file__), 'presets')
        self.preset_manager = PresetManager(presets_dir)
        self.game_controller = GameController()
        self.validator = BindingValidator()
        
        # State
        self.current_parser = None
        self.selected_preset = None
        self.platform = None
        
        # Create backup on first run
        ConfigBackup.create_backup(self.GAME_CONFIG_PATH)
        
        # Detect platform
        self.platform = self.game_controller.detect_platform()
        
        # Build UI
        self._create_ui()
        
        # Load preset list
        self._refresh_preset_list()
    
    def _create_ui(self):
        """Create the main UI layout."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        self._create_sidebar()
        
        # Main area
        self._create_main_area()
        
        # Bottom bar
        self._create_bottom_bar()
    
    def _create_sidebar(self):
        """Create the left sidebar with preset list."""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="RocketBind",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.COLOR_ACCENT
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Preset Manager",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Preset list label
        list_label = ctk.CTkLabel(
            self.sidebar,
            text="Your Presets",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        
        # Preset list
        self.preset_listbox = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color=self.COLOR_BG,
            corner_radius=8
        )
        self.preset_listbox.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        
        # Preset buttons frame
        preset_buttons = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        preset_buttons.grid(row=5, column=0, padx=15, pady=10, sticky="ew")
        preset_buttons.grid_columnconfigure((0, 1), weight=1)
        
        # New preset button
        self.new_preset_btn = ctk.CTkButton(
            preset_buttons,
            text="New",
            command=self._new_preset,
            fg_color=self.COLOR_BLUE,
            hover_color="#0056b3",
            width=100
        )
        self.new_preset_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Import button
        self.import_btn = ctk.CTkButton(
            preset_buttons,
            text="Import",
            command=self._import_preset,
            fg_color=self.COLOR_BLUE,
            hover_color="#0056b3",
            width=100
        )
        self.import_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Duplicate button
        self.duplicate_btn = ctk.CTkButton(
            preset_buttons,
            text="Duplicate",
            command=self._duplicate_preset,
            fg_color="#444444",
            hover_color="#555555",
            width=100,
            state="disabled"
        )
        self.duplicate_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            preset_buttons,
            text="Delete",
            command=self._delete_preset,
            fg_color=self.COLOR_WARNING,
            hover_color="#cc0000",
            width=100,
            state="disabled"
        )
        self.delete_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Platform selector
        platform_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        platform_frame.grid(row=6, column=0, padx=15, pady=(10, 20), sticky="ew")
        
        platform_label = ctk.CTkLabel(
            platform_frame,
            text="Platform:",
            font=ctk.CTkFont(size=12)
        )
        platform_label.pack(pady=(0, 5))
        
        self.platform_var = ctk.StringVar(value=self.platform or "steam")
        self.platform_selector = ctk.CTkSegmentedButton(
            platform_frame,
            values=["steam", "epic"],
            variable=self.platform_var,
            command=self._on_platform_change
        )
        self.platform_selector.pack(pady=5)
    
    def _create_main_area(self):
        """Create the main editing area."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.COLOR_BG)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="No Preset Selected",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.COLOR_ACCENT
        )
        header.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="w")
        self.header_label = header
        
        # Tabview for Gamepad/PC bindings
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color=self.COLOR_SIDEBAR)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Add tabs
        self.tabview.add("Gamepad")
        self.tabview.add("Keyboard/Mouse")
        
        # Gamepad tab
        self.gamepad_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Gamepad"),
            fg_color=self.COLOR_BG
        )
        self.gamepad_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # PC tab
        self.pc_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Keyboard/Mouse"),
            fg_color=self.COLOR_BG
        )
        self.pc_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initially show placeholder
        self._show_placeholder()
    
    def _create_bottom_bar(self):
        """Create the bottom action bar."""
        self.bottom_bar = ctk.CTkFrame(self, corner_radius=0, fg_color=self.COLOR_SIDEBAR, height=80)
        self.bottom_bar.grid(row=1, column=1, sticky="ew", padx=0, pady=0)
        self.bottom_bar.grid_columnconfigure(0, weight=1)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.bottom_bar,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.bottom_bar, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=20, pady=10)
        
        # Save button
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Changes",
            command=self._save_changes,
            fg_color=self.COLOR_BLUE,
            hover_color="#0056b3",
            width=150,
            height=40,
            state="disabled"
        )
        self.save_btn.grid(row=0, column=0, padx=5)
        
        # Apply & Restart button
        self.apply_btn = ctk.CTkButton(
            buttons_frame,
            text="APPLY & RESTART",
            command=self._apply_preset,
            fg_color=self.COLOR_ACCENT,
            hover_color="#ff6600",
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.apply_btn.grid(row=0, column=1, padx=5)
    
    def _show_placeholder(self):
        """Show placeholder when no preset is selected."""
        for widget in self.gamepad_frame.winfo_children():
            widget.destroy()
        for widget in self.pc_frame.winfo_children():
            widget.destroy()
        
        placeholder = ctk.CTkLabel(
            self.gamepad_frame,
            text="Select or create a preset to begin editing",
            font=ctk.CTkFont(size=16),
            text_color="#666666"
        )
        placeholder.pack(pady=100)
    
    def _refresh_preset_list(self):
        """Refresh the preset list in the sidebar."""
        # Clear existing
        for widget in self.preset_listbox.winfo_children():
            widget.destroy()
        
        # Get presets
        presets = self.preset_manager.get_preset_list()
        
        if not presets:
            no_presets = ctk.CTkLabel(
                self.preset_listbox,
                text="No presets yet",
                text_color="#666666",
                font=ctk.CTkFont(size=12)
            )
            no_presets.pack(pady=20)
            return
        
        # Add preset buttons
        for preset_name in presets:
            btn = ctk.CTkButton(
                self.preset_listbox,
                text=preset_name,
                command=lambda p=preset_name: self._load_preset(p),
                fg_color="#2a2a3e",
                hover_color=self.COLOR_BLUE,
                anchor="w",
                height=35
            )
            btn.pack(fill="x", padx=5, pady=2)
    
    def _load_preset(self, preset_name: str):
        """Load a preset for editing."""
        parser = self.preset_manager.load_preset(preset_name)
        
        if parser is None:
            self._set_status(f"Failed to load preset: {preset_name}", error=True)
            return
        
        self.current_parser = parser
        self.selected_preset = preset_name
        self.header_label.configure(text=f"Editing: {preset_name}")
        
        # Enable buttons
        self.save_btn.configure(state="normal")
        self.apply_btn.configure(state="normal")
        self.duplicate_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        
        # Display bindings
        self._display_bindings()
        
        self._set_status(f"Loaded preset: {preset_name}")
    
    def _display_bindings(self):
        """Display current bindings in the UI."""
        if self.current_parser is None:
            return
        
        # Clear existing
        for widget in self.gamepad_frame.winfo_children():
            widget.destroy()
        for widget in self.pc_frame.winfo_children():
            widget.destroy()
        
        # Get bindings
        all_bindings = self.current_parser.get_all_bindings()
        
        # Display gamepad bindings
        self._display_binding_list(
            self.gamepad_frame,
            all_bindings['gamepad'],
            "gamepad"
        )
        
        # Display PC bindings
        self._display_binding_list(
            self.pc_frame,
            all_bindings['pc'],
            "pc"
        )
    
    def _display_binding_list(self, parent, bindings: List[Dict], binding_type: str):
        """Display a list of bindings in a frame."""
        if not bindings:
            label = ctk.CTkLabel(
                parent,
                text=f"No {binding_type} bindings configured",
                text_color="#666666"
            )
            label.pack(pady=20)
            return
        
        # Group by category
        driving_actions = ['ThrottleForward', 'ThrottleReverse', 'SteerLeft', 'SteerRight']
        aerial_actions = ['PitchUp', 'PitchDown', 'YawLeft', 'YawRight', 'RollLeft', 'RollRight']
        camera_actions = ['LookUp', 'LookDown', 'LookLeft', 'LookRight', 'SwivelUp', 'SwivelDown', 'SwivelLeft', 'SwivelRight']
        action_actions = ['Jump', 'Boost', 'Handbrake', 'SecondaryCamera', 'RearCamera', 'ToggleRoll']
        
        categories = [
            ("Driving", driving_actions),
            ("Actions", action_actions),
            ("Aerial", aerial_actions),
            ("Camera", camera_actions),
            ("Other", None)
        ]
        
        for category_name, category_actions in categories:
            # Filter bindings for this category
            if category_actions is None:
                # Other category - all remaining bindings
                category_bindings = [b for b in bindings if b['action'] not in driving_actions + aerial_actions + camera_actions + action_actions]
            else:
                category_bindings = [b for b in bindings if b['action'] in category_actions]
            
            if not category_bindings:
                continue
            
            # Category header
            header = ctk.CTkLabel(
                parent,
                text=category_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.COLOR_ACCENT,
                anchor="w"
            )
            header.pack(fill="x", padx=10, pady=(15, 5))
            
            # Bindings
            for binding in category_bindings:
                self._create_binding_row(parent, binding, binding_type)
    
    def _create_binding_row(self, parent, binding: Dict, binding_type: str):
        """Create a row for a single binding."""
        row_frame = ctk.CTkFrame(parent, fg_color="#2a2a3e", corner_radius=5)
        row_frame.pack(fill="x", padx=10, pady=3)
        
        # Action name
        action_label = ctk.CTkLabel(
            row_frame,
            text=binding['action'],
            font=ctk.CTkFont(size=12),
            width=200,
            anchor="w"
        )
        action_label.pack(side="left", padx=15, pady=10)
        
        # Key display
        key_text = binding.get('key', 'Unbound')
        if binding.get('axis_sign'):
            key_text += f" ({binding['axis_sign']})"
        
        key_label = ctk.CTkLabel(
            row_frame,
            text=key_text,
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_BLUE
        )
        key_label.pack(side="left", padx=10, pady=10)
        
        # Edit button (placeholder for now)
        # In a full implementation, this would open a key binding dialog
        edit_btn = ctk.CTkButton(
            row_frame,
            text="Edit",
            width=60,
            height=25,
            fg_color="#444444",
            hover_color="#555555",
            command=lambda: self._edit_binding(binding, binding_type)
        )
        edit_btn.pack(side="right", padx=10, pady=10)
    
    def _edit_binding(self, binding: Dict, binding_type: str):
        """Edit a binding (simplified for MVP)."""
        # For MVP, just show a message
        self._set_status(f"Editing {binding['action']} - Full key rebinding coming soon!")
    
    def _new_preset(self):
        """Create a new preset."""
        dialog = ctk.CTkInputDialog(
            text="Enter preset name:",
            title="New Preset"
        )
        preset_name = dialog.get_input()
        
        if not preset_name:
            return
        
        if self.preset_manager.create_preset(preset_name):
            self._refresh_preset_list()
            self._load_preset(preset_name)
            self._set_status(f"Created preset: {preset_name}")
        else:
            self._set_status(f"Failed to create preset (name may already exist)", error=True)
    
    def _import_preset(self):
        """Import current settings from game."""
        dialog = ctk.CTkInputDialog(
            text="Enter name for imported preset:",
            title="Import from Game"
        )
        preset_name = dialog.get_input()
        
        if not preset_name:
            return
        
        if self.preset_manager.import_from_game(self.GAME_CONFIG_PATH, preset_name):
            self._refresh_preset_list()
            self._load_preset(preset_name)
            self._set_status(f"Imported current settings as: {preset_name}")
        else:
            self._set_status("Failed to import (check if game config exists)", error=True)
    
    def _duplicate_preset(self):
        """Duplicate the current preset."""
        if not self.selected_preset:
            return
        
        dialog = ctk.CTkInputDialog(
            text=f"Enter name for duplicate of '{self.selected_preset}':",
            title="Duplicate Preset"
        )
        new_name = dialog.get_input()
        
        if not new_name:
            return
        
        if self.preset_manager.duplicate_preset(self.selected_preset, new_name):
            self._refresh_preset_list()
            self._set_status(f"Duplicated '{self.selected_preset}' as '{new_name}'")
        else:
            self._set_status("Failed to duplicate preset", error=True)
    
    def _delete_preset(self):
        """Delete the current preset."""
        if not self.selected_preset:
            return
        
        # Confirmation dialog
        dialog = ctk.CTkInputDialog(
            text=f"Type '{self.selected_preset}' to confirm deletion:",
            title="Delete Preset"
        )
        confirmation = dialog.get_input()
        
        if confirmation != self.selected_preset:
            return
        
        if self.preset_manager.delete_preset(self.selected_preset):
            self._refresh_preset_list()
            self.current_parser = None
            self.selected_preset = None
            self.header_label.configure(text="No Preset Selected")
            self._show_placeholder()
            self.save_btn.configure(state="disabled")
            self.apply_btn.configure(state="disabled")
            self.duplicate_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            self._set_status("Preset deleted")
        else:
            self._set_status("Failed to delete preset", error=True)
    
    def _save_changes(self):
        """Save changes to the current preset."""
        if not self.current_parser or not self.selected_preset:
            return
        
        # Validate
        all_bindings = self.current_parser.get_all_bindings()
        is_valid, errors, warnings = self.validator.validate_bindings(
            all_bindings['gamepad'],
            all_bindings['pc']
        )
        
        if not is_valid:
            error_msg = "Cannot save - validation errors:\n" + "\n".join(errors)
            self._set_status(error_msg, error=True)
            return
        
        # Save
        if self.preset_manager.save_preset(self.selected_preset, self.current_parser):
            self._set_status(f"Saved changes to {self.selected_preset}")
        else:
            self._set_status("Failed to save preset", error=True)
    
    def _apply_preset(self):
        """Apply preset and restart game."""
        if not self.current_parser or not self.selected_preset:
            return
        
        # Validate first
        all_bindings = self.current_parser.get_all_bindings()
        is_valid, errors, warnings = self.validator.validate_bindings(
            all_bindings['gamepad'],
            all_bindings['pc']
        )
        
        if not is_valid:
            error_msg = "Cannot apply - validation errors:\n" + "\n".join(errors)
            self._set_status(error_msg, error=True)
            return
        
        # Show warnings if any
        if warnings:
            self._set_status(f"Warning: {warnings[0]}")
        
        # Check if game is running
        if self.game_controller.is_game_running():
            self.apply_btn.configure(text="CLOSING GAME...", state="disabled")
            self.update()
        
        # Apply
        platform = self.platform_var.get()
        success, message = self.game_controller.apply_preset_and_restart(
            self.current_parser,
            self.GAME_CONFIG_PATH,
            platform
        )
        
        self.apply_btn.configure(text="APPLY & RESTART", state="normal")
        
        if success:
            self._set_status(message)
        else:
            self._set_status(message, error=True)
    
    def _on_platform_change(self, value):
        """Handle platform selection change."""
        self.platform = value
        self.game_controller.platform = value
    
    def _set_status(self, message: str, error: bool = False):
        """Set status message."""
        color = self.COLOR_WARNING if error else "#888888"
        self.status_label.configure(text=message, text_color=color)
