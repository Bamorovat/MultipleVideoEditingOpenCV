"""
Configuration settings for Multiple Video Editing tool
@author Mohammad Abadi <m.bamorovvat@gmail.com>
"""

import os
import numpy as np


class Color:
    """Terminal color codes for formatted output."""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Config:
    """Configuration class containing all settings and constants."""
    
    # Default paths
    DEFAULT_VIDEO_PATH = '/home/abbas/phd/dataset/video/'
    DEFAULT_ACTION_PATH = '/home/abbas/phd/dataset/action/'
    
    # Camera view subdirectories
    CAMERA_VIEWS = {
        'robot_view': 'robot_view/',
        'rgbd_livingroom': 'rgbd_livingroom/',
        'omni_livingroom': 'omni_livingroom/',
        'rgbd_sofa': 'rgbd_sofa/'
    }
    
    # Frame trimming offsets for synchronization
    TRIMMING_OFFSETS = {
        'robot_view': 0,
        'living_room_view': 0,
        'omni_view': 50,
        'sofa_view': 0
    }
    
    # Video recording settings
    VIDEO_CODEC = 'MJPG'
    FRAME_RATE = 30.0
    
    # Video dimensions for each camera
    VIDEO_DIMENSIONS = {
        'robot_view': (640, 480),
        'rgbd_livingroom': (640, 480),
        'omni_livingroom': (512, 486),
        'rgbd_sofa': (640, 480)
    }
    
    # Default frame control settings
    DEFAULT_FRAME_NUMBER = 260
    DEFAULT_PLAYBACK_RATE = 30
    
    # Control panel settings
    CONTROL_PANEL_SIZE = (50, 750, 3)
    CONTROL_TEXT = "W: Play | S: Stay | A: Prev | D: Next | Z: Frame_Start | X: Frame_End | C: Snap | Esc: Exit"
    CONTROL_FONT = 1  # cv2.FONT_HERSHEY_COMPLEX
    CONTROL_FONT_SCALE = 0.45
    CONTROL_TEXT_COLOR = (100, 140, 60)
    CONTROL_TEXT_POSITION = (40, 30)
    
    # Window positions
    WINDOW_POSITIONS = {
        'controls': (500, 40),
        'robot_view': (100, 40),
        'rgbd_livingroom': (750, 40),
        'omni_livingroom': (1400, 40),
        'rgbd_sofa': (1400, 700)
    }
    
    # Key mappings
    KEY_MAPPINGS = {
        # Play/Pause controls
        ord('s'): 'stay', ord('S'): 'stay',
        ord('w'): 'play', ord('W'): 'play',
        
        # Frame navigation
        ord('a'): 'prev_frame', ord('A'): 'prev_frame',
        ord('d'): 'next_frame', ord('D'): 'next_frame',
        
        # Speed controls
        ord('q'): 'slow', ord('Q'): 'slow',
        ord('e'): 'fast', ord('E'): 'fast',
        
        # Recording controls
        ord('z'): 'Frame_Start', ord('Z'): 'Frame_Start',
        ord('x'): 'Frame_End', ord('X'): 'Frame_End',
        
        # Utility controls
        ord('c'): 'snap', ord('C'): 'snap',
        27: 'exit'  # ESC key
    }
    
    @classmethod
    def get_video_paths(cls, base_path):
        """Generate video input paths."""
        return {
            view: os.path.join(base_path, subdir)
            for view, subdir in cls.CAMERA_VIEWS.items()
        }
    
    @classmethod
    def get_action_paths(cls, base_path):
        """Generate action output paths."""
        return {
            view: os.path.join(base_path, subdir)
            for view, subdir in cls.CAMERA_VIEWS.items()
        }
    
    @classmethod
    def create_control_panel(cls):
        """Create and return the control panel with instructions."""
        controls = np.zeros(cls.CONTROL_PANEL_SIZE, np.uint8)
        return controls
