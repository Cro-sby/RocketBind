"""
Validation logic for RocketBind.
Ensures bindings are valid and don't conflict.
"""
from typing import List, Dict, Tuple


class BindingValidator:
    """Validate control bindings."""
    
    ESSENTIAL_ACTIONS = [
        'ThrottleForward',
        'ThrottleReverse', 
        'SteerLeft',
        'SteerRight',
        'Jump',
        'Boost',
        'Handbrake'
    ]
    
    CAMERA_ACTIONS = [
        'LookUp',
        'LookDown',
        'LookLeft',
        'LookRight',
        'SwivelUp',
        'SwivelDown',
        'SwivelLeft',
        'SwivelRight'
    ]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_bindings(self, gamepad_bindings: List[Dict], pc_bindings: List[Dict]) -> Tuple[bool, List[str], List[str]]:
        """Validate all bindings and return (is_valid, errors, warnings)."""
        self.errors = []
        self.warnings = []
        
        # Check for essential actions
        self._check_essential_actions(gamepad_bindings, pc_bindings)
        
        # Check for conflicts in gamepad
        self._check_conflicts(gamepad_bindings, 'Gamepad')
        
        # Check for conflicts in PC
        self._check_conflicts(pc_bindings, 'PC')
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors.copy(), self.warnings.copy()
    
    def _check_essential_actions(self, gamepad_bindings: List[Dict], pc_bindings: List[Dict]):
        """Check if all essential actions are bound."""
        # Check gamepad essential actions
        gamepad_actions = {b['action'] for b in gamepad_bindings if b.get('key')}
        missing_gamepad = [a for a in self.ESSENTIAL_ACTIONS if a not in gamepad_actions]
        
        if missing_gamepad:
            self.errors.append(f"Gamepad missing essential bindings: {', '.join(missing_gamepad)}")
        
        # Check PC essential actions
        pc_actions = {b['action'] for b in pc_bindings if b.get('key')}
        missing_pc = [a for a in self.ESSENTIAL_ACTIONS if a not in pc_actions]
        
        if missing_pc:
            self.errors.append(f"PC missing essential bindings: {', '.join(missing_pc)}")
    
    def _check_conflicts(self, bindings: List[Dict], device_type: str):
        """Check for conflicting key bindings."""
        key_to_actions = {}
        
        for binding in bindings:
            key = binding.get('key')
            action = binding.get('action')
            
            if not key or not action:
                continue
            
            # Build a unique key identifier including axis sign if present
            key_id = key
            if binding.get('axis_sign'):
                key_id = f"{key}_{binding['axis_sign']}"
            
            # Skip certain actions that can share keys (like camera controls)
            if action in self.CAMERA_ACTIONS:
                continue
            
            if key_id not in key_to_actions:
                key_to_actions[key_id] = []
            key_to_actions[key_id].append(action)
        
        # Report conflicts
        for key_id, actions in key_to_actions.items():
            if len(actions) > 1:
                # Check if all conflicting actions are in the same "family"
                if not self._are_actions_compatible(actions):
                    self.warnings.append(f"{device_type}: Key '{key_id}' is bound to multiple actions: {', '.join(actions)}")
    
    def _are_actions_compatible(self, actions: List[str]) -> bool:
        """Check if multiple actions can share the same key."""
        # Steer and Yaw can share keys
        steer_yaw = {'SteerLeft', 'SteerRight', 'YawLeft', 'YawRight'}
        if all(a in steer_yaw for a in actions):
            return True
        
        # Throttle and Pitch can share keys
        throttle_pitch = {'ThrottleForward', 'ThrottleReverse', 'PitchUp', 'PitchDown'}
        if all(a in throttle_pitch for a in actions):
            return True
        
        return False
    
    def check_single_binding(self, action: str, key: str, existing_bindings: List[Dict]) -> Tuple[bool, str]:
        """Check if a single binding would cause conflicts."""
        for binding in existing_bindings:
            if binding['action'] == action:
                continue  # Skip the action we're trying to bind
            
            if binding.get('key') == key:
                # Check if they're compatible
                if not self._are_actions_compatible([action, binding['action']]):
                    return False, f"Key '{key}' is already bound to '{binding['action']}'"
        
        return True, ""
