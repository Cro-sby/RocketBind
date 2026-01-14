"""
Game control utilities for RocketBind.
Handles process management and game launching.
"""
import os
import subprocess
import psutil
import time
from typing import Tuple, Optional


class GameController:
    """Control Rocket League process and launching."""
    
    PROCESS_NAME = "RocketLeague.exe"
    STEAM_URI = "steam://rungameid/252950"
    EPIC_URI = "com.epicgames.launcher://apps/Sugar?action=launch&silent=true"
    
    def __init__(self):
        self.platform = None  # Will be 'steam' or 'epic'
    
    def is_game_running(self) -> bool:
        """Check if Rocket League is currently running."""
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == self.PROCESS_NAME:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def kill_game(self) -> bool:
        """Kill Rocket League process."""
        try:
            # Use taskkill command for forceful termination
            result = subprocess.run(
                ['taskkill', '/F', '/IM', self.PROCESS_NAME],
                capture_output=True,
                text=True
            )
            
            # Wait a moment for process to fully terminate
            time.sleep(1)
            
            return result.returncode == 0 or not self.is_game_running()
        except Exception as e:
            print(f"Error killing game process: {e}")
            return False
    
    def detect_platform(self) -> Optional[str]:
        """Detect if user has Steam or Epic version."""
        # Check Steam install
        steam_path = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague"
        steam_path_alt = r"C:\Program Files\Steam\steamapps\common\rocketleague"
        
        # Check Epic install
        epic_path = r"C:\Program Files\Epic Games\rocketleague"
        
        if os.path.exists(steam_path) or os.path.exists(steam_path_alt):
            self.platform = 'steam'
            return 'steam'
        elif os.path.exists(epic_path):
            self.platform = 'epic'
            return 'epic'
        
        # If not found, try to detect from registry or ask user
        return None
    
    def launch_game(self, platform: str = None) -> bool:
        """Launch Rocket League using the appropriate platform."""
        if platform is None:
            platform = self.platform or self.detect_platform()
        
        if platform is None:
            return False
        
        try:
            if platform == 'steam':
                os.startfile(self.STEAM_URI)
            elif platform == 'epic':
                os.startfile(self.EPIC_URI)
            else:
                return False
            
            return True
        except Exception as e:
            print(f"Error launching game: {e}")
            return False
    
    def apply_preset_and_restart(self, preset_parser, game_config_path: str, platform: str = None) -> Tuple[bool, str]:
        """
        Complete workflow: kill game, apply preset, restart game.
        Returns (success, message)
        """
        # Step 1: Check if game is running
        was_running = self.is_game_running()
        
        if was_running:
            # Step 2: Kill the game
            if not self.kill_game():
                return False, "Failed to close Rocket League"
            
            # Wait for process to fully terminate
            time.sleep(1.5)
        
        # Step 3: Apply the preset (write to TAInput.ini)
        try:
            # Remove read-only attribute if present
            if os.path.exists(game_config_path):
                os.chmod(game_config_path, 0o666)
            
            # Write the preset
            if not preset_parser.write_file(game_config_path):
                return False, "Failed to write configuration file"
        except Exception as e:
            return False, f"Error writing config: {e}"
        
        # Step 4: Relaunch the game if it was running
        if was_running:
            time.sleep(0.5)
            if not self.launch_game(platform):
                return False, "Preset applied but failed to relaunch game"
            
            return True, "Preset applied and game restarted successfully!"
        else:
            return True, "Preset applied successfully! Launch game to use it."


class ConfigBackup:
    """Handle backup of TAInput.ini file."""
    
    @staticmethod
    def create_backup(source_path: str) -> bool:
        """Create a backup of the config file."""
        if not os.path.exists(source_path):
            return False
        
        backup_path = source_path + ".bak"
        
        # Don't overwrite existing backup
        if os.path.exists(backup_path):
            return True
        
        try:
            import shutil
            shutil.copy2(source_path, backup_path)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    @staticmethod
    def restore_backup(config_path: str) -> bool:
        """Restore from backup."""
        backup_path = config_path + ".bak"
        
        if not os.path.exists(backup_path):
            return False
        
        try:
            import shutil
            # Remove read-only if present
            if os.path.exists(config_path):
                os.chmod(config_path, 0o666)
            
            shutil.copy2(backup_path, config_path)
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
