"""
Multiple Video Editor - Main class implementation
@author Mohammad Abadi <m.bamorovvat@gmail.com>
"""

import cv2
import os
import numpy as np
from time import sleep
from ..config import Config, Color


class MultipleVideoEditor:
    """
    A comprehensive multiple video editing tool for synchronizing and processing
    multiple camera views for human activity recognition research.
    """
    
    def __init__(self, video_path=None, action_path=None):
        """
        Initialize the Multiple Video Editor with paths and default settings.
        
        Args:
            video_path (str): Base path for input videos
            action_path (str): Base path for output action videos
        """
        # Use provided paths or defaults from config
        self.video_path = video_path or Config.DEFAULT_VIDEO_PATH
        self.action_path = action_path or Config.DEFAULT_ACTION_PATH
        
        # Generate camera-specific paths
        self.video_paths = Config.get_video_paths(self.video_path)
        self.action_paths = Config.get_action_paths(self.action_path)
        
        # Video capture objects
        self.caps = {
            'robot_view': None,
            'rgbd_livingroom': None,
            'omni_livingroom': None,
            'rgbd_sofa': None
        }
        
        # Video writer objects
        self.writers = {
            'robot_view': None,
            'rgbd_livingroom': None,
            'omni_livingroom': None,
            'rgbd_sofa': None
        }
        
        # Control variables
        self.check = None
        self.status = 'stay'
        self.off = 0
        
        # Frame control variables
        self.livingroom_frame_number = Config.DEFAULT_FRAME_NUMBER
        self.tots = 0
        self.frame_rate = Config.DEFAULT_PLAYBACK_RATE
        self.frame_start = 0
        self.frame_end = 0
        
        # Frame totals for each camera
        self.frame_totals = {
            'robot_view': 0,
            'rgbd_livingroom': 0,
            'omni_livingroom': 0,
            'rgbd_sofa': 0
        }
        
        # Control panel
        self.controls = Config.create_control_panel()
    
    def get_videos(self, cap_name):
        """Load video capture objects for all camera views."""
        for view, path in self.video_paths.items():
            video_file = os.path.join(path, f"{cap_name}.avi")
            self.caps[view] = cv2.VideoCapture(video_file)

    def frame_count(self):
        """Get frame counts for all video captures."""
        for view, cap in self.caps.items():
            if cap is not None:
                self.frame_totals[view] = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    def create_trackbar(self, frame_total, frame_name1, frame_name2, window_name):
        """Create trackbars for frame control."""
        cv2.createTrackbar(frame_name1, window_name, 0, int(frame_total) - 1, self._flick_callback)
        cv2.createTrackbar(frame_name2, window_name, 1, 100, self._flick_callback)
        cv2.setTrackbarPos(frame_name1, window_name, 0)
        cv2.setTrackbarPos(frame_name2, window_name, self.frame_rate)

    def _flick_callback(self, val):
        """Trackbar callback function."""
        pass

    def initialize_player(self):
        """Initialize the video player interface."""
        # Create windows
        window_names = ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa', 'controls']
        for window in window_names:
            cv2.namedWindow(window)
        
        # Position windows
        for window, position in Config.WINDOW_POSITIONS.items():
            cv2.moveWindow(window, position[0], position[1])

        # Add control text
        cv2.putText(self.controls, Config.CONTROL_TEXT, Config.CONTROL_TEXT_POSITION,
                   Config.CONTROL_FONT, Config.CONTROL_FONT_SCALE, Config.CONTROL_TEXT_COLOR)

        # Initialize frame counting and trackbars
        self.frame_count()
        
        trackbar_windows = ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa']
        for window in trackbar_windows:
            frame_total = self.frame_totals.get(window, 0)
            self.create_trackbar(frame_total, 'Frame_number', 'Frame_rate', window)

    def get_trackbar_positions(self):
        """Get trackbar positions and apply frame rate delay."""
        frame_rates = []
        for window in ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa']:
            frame_rates.append(cv2.getTrackbarPos('Frame_rate', window))
        
        for rate in frame_rates:
            sleep((0.1 - rate / 1000.0) ** 21021)

    def set_trackbar_positions(self, mode, value):
        """Set trackbar positions for synchronization."""
        if mode == 'frame':
            offsets = Config.TRIMMING_OFFSETS
            cv2.setTrackbarPos('Frame_number', 'robot_view', value + offsets['robot_view'])
            cv2.setTrackbarPos('Frame_number', 'rgbd_livingroom', value + offsets['living_room_view'])
            cv2.setTrackbarPos('Frame_number', 'omni_livingroom', value + offsets['omni_view'])
            cv2.setTrackbarPos('Frame_number', 'rgbd_sofa', value + offsets['sofa_view'])
        elif mode == 'rate':
            for window in ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa']:
                cv2.setTrackbarPos('Frame_rate', window, value)

    def initialize_recording(self):
        """Initialize video recording objects."""
        class_name = self._get_class_name()
        file_name = str(self._get_next_file_number(self.action_paths['robot_view'], class_name))
        
        fourcc = cv2.VideoWriter_fourcc(*Config.VIDEO_CODEC)
        
        for view in self.writers.keys():
            output_path = os.path.join(self.action_paths[view], class_name, f"{file_name}.avi")
            dimensions = Config.VIDEO_DIMENSIONS[view]
            self.writers[view] = cv2.VideoWriter(output_path, fourcc, Config.FRAME_RATE, dimensions)

    def _create_class_folders(self, class_name):
        """Create folders for new action class."""
        for path in self.action_paths.values():
            dir_path = os.path.join(path, class_name)
            os.makedirs(dir_path, exist_ok=True)
        print("Successfully Created the Class Directory")

    def _get_class_name(self):
        """Get or create class name for action recording."""
        class_name_confirmation = 'n'
        
        while class_name_confirmation != 'y':
            class_list_path = os.path.join(self.action_path, 'Class_List.txt')
            
            if not os.path.exists(class_list_path):
                with open(class_list_path, 'w') as f:
                    f.write("")
            
            with open(class_list_path, 'r+') as class_list:
                existing_classes = class_list.readlines()
                
                print(Color.BOLD + Color.DARKCYAN + 'Existing Classes Are: ' + Color.END)
                for i, line in enumerate(existing_classes, start=1):
                    print(f'{Color.CYAN}{i} = {line.strip()}{Color.END}')
                
                class_name = input("What is The Class Name or Number: ")
                
                if class_name.isdigit():
                    print('You entered the Class Number ...')
                    try:
                        class_name = existing_classes[int(class_name) - 1].strip()
                    except (IndexError, ValueError):
                        print('Invalid class number!')
                        continue
                
                print(f"The Class name is: {Color.BOLD}{Color.RED}{Color.UNDERLINE}{class_name}{Color.END}")
                class_name_confirmation = input('Is it the correct class name (y/n)? ')
                
                if class_name_confirmation == 'y':
                    print(" Checking for the class ...")
                    class_exists = any(class_name in line for line in existing_classes)
                    
                    if not class_exists:
                        print(" The New Class is Adding ...")
                        self._create_class_folders(class_name)
                        class_list.write(class_name + '\n')
                        print("The New Class is Added")
                    else:
                        print("The Class already exists")
                        
                elif class_name_confirmation != 'n':
                    print('Error: Enter (y/n) ...')
        
        return class_name

    def _get_next_file_number(self, folder_path, class_name):
        """Get the next available file number for recording."""
        action_class_path = os.path.join(folder_path, class_name)
        highest_num = 0
        
        if os.path.exists(action_class_path):
            for filename in os.listdir(action_class_path):
                if os.path.isfile(os.path.join(action_class_path, filename)):
                    name_without_ext = os.path.splitext(filename)[0]
                    try:
                        file_num = int(name_without_ext)
                        highest_num = max(highest_num, file_num)
                    except ValueError:
                        continue
        
        return highest_num + 1

    def record_video_segment(self):
        """Record video segments from all cameras."""
        self.initialize_recording()
        length = self.frame_end - self.frame_start
        
        # Set starting positions for all cameras
        offsets = Config.TRIMMING_OFFSETS
        cameras = ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa']
        offset_keys = ['robot_view', 'living_room_view', 'omni_view', 'sofa_view']
        
        for cam, offset_key in zip(cameras, offset_keys):
            if self.caps[cam]:
                self.caps[cam].set(cv2.CAP_PROP_POS_FRAMES, self.frame_start + offsets[offset_key])
        
        # Record frames
        for _ in range(length):
            for cam in cameras:
                if self.caps[cam] and self.writers[cam]:
                    ret, frame = self.caps[cam].read()
                    if ret:
                        self.writers[cam].write(frame)

        # Release writers
        for writer in self.writers.values():
            if writer:
                writer.release()

    def save_snapshots(self, frames, action_name):
        """Save snapshot images from all cameras."""
        filenames = {
            'robot_view': f"./Snap_robot_view_{action_name}.jpg",
            'rgbd_livingroom': f"./Snap_living_room_{action_name}.jpg",
            'omni_livingroom': f"./Snap_omni_view_{action_name}.jpg",
            'rgbd_sofa': f"./Snap_sofa_view_{action_name}.jpg"
        }
        
        for view, frame in frames.items():
            if frame is not None:
                cv2.imwrite(filenames[view], frame)

    def play_videos(self):
        """Main playback loop with user controls."""
        cv2.imshow("controls", self.controls)

        try:
            if self.livingroom_frame_number >= self.tots - 1:
                self.livingroom_frame_number = 0
                
            # Set frame positions
            offsets = Config.TRIMMING_OFFSETS
            cameras = ['robot_view', 'rgbd_livingroom', 'omni_livingroom', 'rgbd_sofa']
            offset_keys = ['robot_view', 'living_room_view', 'omni_view', 'sofa_view']
            
            frames = {}
            for cam, offset_key in zip(cameras, offset_keys):
                if self.caps[cam]:
                    self.caps[cam].set(cv2.CAP_PROP_POS_FRAMES, 
                                     self.livingroom_frame_number + offsets[offset_key])
                    ret, frame = self.caps[cam].read()
                    frames[cam] = frame if ret else None

            # Display frames
            window_positions = Config.WINDOW_POSITIONS
            for cam, frame in frames.items():
                if frame is not None:
                    cv2.imshow(cam, frame)

            # Handle user input
            key = cv2.waitKey(10)
            self.status = Config.KEY_MAPPINGS.get(key, self.status)

            self.set_trackbar_positions('frame', self.livingroom_frame_number)

            # Execute actions based on status
            self._handle_playback_control(frames)

        except Exception as e:
            print(f"Error during playback: {e}")

    def _handle_playback_control(self, frames):
        """Handle different playback control actions."""
        if self.status == 'play':
            self.get_trackbar_positions()
            self.livingroom_frame_number += 1
            self.set_trackbar_positions('frame', self.livingroom_frame_number)
        elif self.status == 'stay':
            self.livingroom_frame_number = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
        elif self.status == 'exit':
            self.cleanup()
        elif self.status == 'prev_frame':
            self.livingroom_frame_number = max(0, self.livingroom_frame_number - 1)
            self.set_trackbar_positions('frame', self.livingroom_frame_number)
            self.status = 'stay'
        elif self.status == 'next_frame':
            self.livingroom_frame_number += 1
            self.set_trackbar_positions('frame', self.livingroom_frame_number)
            self.status = 'stay'
        elif self.status == 'Frame_Start':
            self.frame_start = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
            print(Color.BLUE + "################## Start Capturing ################# " + Color.END)
            print(f"The Start Frame Number is: {Color.BOLD}{Color.PURPLE}{self.frame_start}{Color.END}")
            self.status = 'stay'
        elif self.status == 'Frame_End':
            self.frame_end = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
            print(f"The Last Frame Number is: {Color.BOLD}{Color.PURPLE}{self.frame_end}{Color.END}")
            print(' Please Wait ... ')
            print(' The Videos Are Saving ... ')
            self.record_video_segment()
            print('The Videos Are Saved ')
            print(Color.YELLOW + "################## End Capturing ################# " + Color.END)
            self.status = 'stay'
        elif self.status == 'slow':
            self.frame_rate = max(self.frame_rate - 5, 0)
            self.set_trackbar_positions('rate', self.frame_rate)
            self.status = 'play'
        elif self.status == 'fast':
            self.frame_rate = min(100, self.frame_rate + 5)
            self.set_trackbar_positions('rate', self.frame_rate)
            self.status = 'play'
        elif self.status == 'snap':
            action_name = input('What is the action name? ')
            self.save_snapshots(frames, action_name)
            print(f"Snap of Frame {self.livingroom_frame_number} Taken!")
            self.status = 'stay'

    def cleanup(self):
        """Clean up resources and close windows."""
        self.off = 1
        
        # Release video captures
        for cap in self.caps.values():
            if cap:
                cap.release()
        
        # Release video writers
        for writer in self.writers.values():
            if writer:
                writer.release()

        cv2.destroyAllWindows()

    def run(self, video_name='10'):
        """Main execution method."""
        print(f"Loading videos: {video_name}")
        self.get_videos(video_name)
        self.initialize_player()

        print("Starting video editor...")
        print("Use keyboard controls to navigate and edit videos.")
        
        while self.off == 0:
            self.play_videos()
        
        print("Video editor closed.")
