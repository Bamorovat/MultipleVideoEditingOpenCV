"""
Multiple Video Editing tool - Main entry point
@author Mohammad Abadi <m.bamorovvat@gmail.com>
"""

import sys
import argparse
from src.core import MultipleVideoEditor
from src.config import Config, Color


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Multiple Video Editing tool for synchronized multi-camera editing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Use default video '10'
  python main.py --video 15              # Load video '15'
  python main.py --video-path /custom/path --action-path /output/path
  
Controls:
  W: Play          | S: Stay (Pause)    | A: Previous Frame | D: Next Frame
  Z: Start Frame   | X: End Frame       | C: Take Snapshot  | ESC: Exit
  Q: Slower        | E: Faster
        """
    )
    
    parser.add_argument(
        '--video', '-v',
        type=str,
        default='10',
        help='Video name to load (default: 10)'
    )
    
    parser.add_argument(
        '--video-path',
        type=str,
        default=Config.DEFAULT_VIDEO_PATH,
        help=f'Base path for input videos (default: {Config.DEFAULT_VIDEO_PATH})'
    )
    
    parser.add_argument(
        '--action-path',
        type=str,
        default=Config.DEFAULT_ACTION_PATH,
        help=f'Base path for output action videos (default: {Config.DEFAULT_ACTION_PATH})'
    )
    
    parser.add_argument(
        '--list-config',
        action='store_true',
        help='Show current configuration and exit'
    )
    
    return parser.parse_args()


def show_configuration(video_path, action_path):
    """Display current configuration."""
    print(f"{Color.BOLD}{Color.CYAN}Multiple Video Editor Configuration{Color.END}")
    print("=" * 50)
    print(f"Video Path: {Color.GREEN}{video_path}{Color.END}")
    print(f"Action Path: {Color.GREEN}{action_path}{Color.END}")
    print(f"\nCamera Views:")
    for view, subdir in Config.CAMERA_VIEWS.items():
        print(f"  {Color.YELLOW}{view}{Color.END}: {video_path}{subdir}")
    
    print(f"\nTrimming Offsets:")
    for view, offset in Config.TRIMMING_OFFSETS.items():
        print(f"  {Color.YELLOW}{view}{Color.END}: {offset} frames")
    
    print(f"\nVideo Settings:")
    print(f"  Codec: {Config.VIDEO_CODEC}")
    print(f"  Frame Rate: {Config.FRAME_RATE}")
    
    print(f"\nDimensions:")
    for view, dims in Config.VIDEO_DIMENSIONS.items():
        print(f"  {Color.YELLOW}{view}{Color.END}: {dims[0]}x{dims[1]}")


def main():
    """Main function."""
    try:
        args = parse_arguments()
        
        # Show configuration if requested
        if args.list_config:
            show_configuration(args.video_path, args.action_path)
            return 0
        
        # Print welcome message
        print(f"{Color.BOLD}{Color.BLUE}Multiple Video Editor{Color.END}")
        print(f"Author: Mohammad Abadi <m.bamorovvat@gmail.com>")
        print("=" * 50)
        
        # Validate paths
        import os
        if not os.path.exists(args.video_path):
            print(f"{Color.RED}Error: Video path does not exist: {args.video_path}{Color.END}")
            return 1
        
        # Create action path if it doesn't exist
        os.makedirs(args.action_path, exist_ok=True)
        
        # Initialize and run the editor
        editor = MultipleVideoEditor(
            video_path=args.video_path,
            action_path=args.action_path
        )
        
        print(f"Loading video: {Color.GREEN}{args.video}{Color.END}")
        print(f"Video path: {Color.CYAN}{args.video_path}{Color.END}")
        print(f"Action path: {Color.CYAN}{args.action_path}{Color.END}")
        print("\nPress any key in the video windows to start...")
        
        editor.run(args.video)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}Interrupted by user{Color.END}")
        return 1
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
