# Multiple Video Editing OpenCV

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Bamorovat/MultipleVideoEditingOpenCV)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0%2B-green.svg)](https://opencv.org/)

## Author: [Mohammad Hossein Bamorovat Abadi](https://www.bamorovat.com/)
This work is a part of the Human Activity Recognition project at [Robot House](https://robothouse.herts.ac.uk/)

**Project Page:** [RHM Dataset](https://bamorovat.com/projects/rhm-dataset.html)

This code is implemented with **Python programming Language** and **OpenCV Library**.

## Citation

> [!IMPORTANT]
> If you use the RHM dataset or this code in your research, please cite the relevant papers below.

### Primary Dataset Paper
**Mohammad Hossein Bamorovat Abadi**, Mohamad Reza Shahabian Alashti, Patrick Holthaus, Catherine Menon, and Farshid Amirabdollahian. "RHM: Robot House Multi-view Human Activity Recognition Dataset." *ACHI 2023, Venice, Italy, IARIA.*

**BibTeX:**
```bibtex
@inproceedings{bamorovat2023rhm,
  title={RHM: Robot House Multi-view Human Activity Recognition Dataset},
  author={Bamorovat Abadi, Mohammad Hossein and Shahabian Alashti, Mohamad Reza and Holthaus, Patrick and Menon, Catherine and Amirabdollahian, Farshid},
  booktitle={ACHI 2023: The Sixteenth International Conference on Advances in Computer-Human Interactions},
  year={2023},
  organization={IARIA},
  address={Venice, Italy}
}
```

### Additional Related Publications

**Mohammad Hossein Bamorovat Abadi**, Mohamad Reza Shahabian Alashti, Patrick Holthaus, Catherine Menon, and Farshid Amirabdollahian. "Robot house human activity recognition dataset." *4th UK-RAS Conference: Robotics at Home (UKRAS21), 19–20. Hatfield, UK, 2021.*

**BibTeX:**
```bibtex
@inproceedings{bamorovat2021robot,
  title={Robot house human activity recognition dataset},
  author={Bamorovat Abadi, Mohammad Hossein and Shahabian Alashti, Mohamad Reza and Holthaus, Patrick and Menon, Catherine and Amirabdollahian, Farshid},
  booktitle={4th UK-RAS Conference: Robotics at Home (UKRAS21)},
  pages={19--20},
  year={2021},
  address={Hatfield, UK}
}
```

**Mohammad Hossein Bamorovat Abadi**, Mohamad Reza Shahabian Alashti, Patrick Holthaus, Catherine Menon, and Farshid Amirabdollahian. "Robotic Vision and Multi-View Synergy: Action and activity recognition in assisted living scenarios." *BioRob 2024, Heidelberg, Germany, IEEE.*

**BibTeX:**
```bibtex
@inproceedings{bamorovat2024robotic,
  title={Robotic Vision and Multi-View Synergy: Action and activity recognition in assisted living scenarios},
  author={Bamorovat Abadi, Mohammad Hossein and Shahabian Alashti, Mohamad Reza and Holthaus, Patrick and Menon, Catherine and Amirabdollahian, Farshid},
  booktitle={2024 10th IEEE RAS/EMBS International Conference on Biomedical Robotics and Biomechatronics (BioRob)},
  year={2024},
  organization={IEEE},
  address={Heidelberg, Germany}
}
```

## License

> [!IMPORTANT]
> This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

> [!TIP]
> When contributing, ensure your code follows the existing modular structure and includes appropriate documentation.


## Installation

> [!IMPORTANT]
> This tool requires Python 3.8+ and OpenCV 4.0+ for optimal performance.

```bash
# Clone the repository
git clone https://github.com/Bamorovat/MultipleVideoEditingOpenCV.git
cd MultipleVideoEditingOpenCV

# Install dependencies
pip install -r requirements.txt
```

## Usage

The tool features a **modern modular architecture** with separate configuration and core logic components.

> [!TIP]
> Use the command line interface for the best experience with built-in help and configuration options.

### Quick Start

**Option 1: Command Line Interface (Recommended)**
```bash
# Basic usage with default video '10'
python main.py

# Specify a different video
python main.py --video 15

# Custom paths
python main.py --video-path /path/to/videos --action-path /path/to/output

# Show configuration
python main.py --list-config

# Help
python main.py --help
```

**Option 2: Programmatic Usage**
```python
from src.core import MultipleVideoEditor

# Initialize the editor
editor = MultipleVideoEditor()

# Run with default video '10'
editor.run()

# Or specify custom paths and video
editor = MultipleVideoEditor(
    video_path='/custom/video/path/',
    action_path='/custom/action/path/'
)
editor.run('your_video_name')
```

### Project Structure

The project is organized with a **clean modular folder structure**:

```
MultipleVideoEditingOpenCV/
├── main.py                    # Entry point with CLI interface
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
└── src/                       # Source code package
    ├── __init__.py
    ├── config/                # Configuration module
    │   ├── __init__.py
    │   └── config.py          # Settings, constants, and color definitions
    └── core/                  # Core functionality module
        ├── __init__.py
        └── video_editor.py    # Main MultipleVideoEditor class
```

**Key Components:**
- **`main.py`**: Entry point with command-line interface and argument parsing
- **`src/core/video_editor.py`**: Core `MultipleVideoEditor` class with all video processing logic
- **`src/config/config.py`**: Configuration settings, constants, and color definitions

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated config and core logic
- **Multi-camera Support**: Synchronize and edit videos from 4 different camera views:
  - Robot view camera
  - RGB living room camera  
  - Omnidirectional living room camera
  - Sofa view camera
- **Interactive Controls**: 
  - `W`: Play | `S`: Stay/Pause | `A`: Previous Frame | `D`: Next Frame
  - `Z`: Set Start Frame | `X`: Set End Frame & Record | `C`: Take Snapshot
  - `Q`: Slower | `E`: Faster | `Esc`: Exit
- **📂 Action Classification**: Organize recorded segments by action classes with automatic folder creation
- **Frame Synchronization**: Configurable trimming offsets for perfect camera synchronization
- **Command Line Interface**: Full CLI with help, configuration display, and path customization
- **Flexible Configuration**: Easily customizable paths, dimensions, codecs, and settings

## Configuration

The tool uses a centralized configuration system in `src/config/config.py`. Key settings include:

- **Camera Views**: Robot, RGB livingroom, Omni livingroom, Sofa
- **Trimming Offsets**: Frame synchronization offsets for each camera
- **Video Settings**: Codec (MJPG), frame rate (30 FPS), dimensions per camera
- **Control Mappings**: Keyboard shortcuts and window positions

> [!TIP]
> You can customize paths, camera settings, and synchronization offsets in the configuration file without modifying the core logic.

## Video Dataset Requirements

> [!WARNING]
> Ensure your video dataset follows the expected directory structure with synchronized multi-camera recordings.

Expected directory structure:
```
video_dataset/
├── robot_view/
│   ├── 10.avi
│   ├── 15.avi
│   └── ...
├── rgbd_livingroom/
│   ├── 10.avi
│   ├── 15.avi
│   └── ...
├── omni_livingroom/
│   ├── 10.avi
│   ├── 15.avi
│   └── ...
└── rgbd_sofa/
    ├── 10.avi
    ├── 15.avi
    └── ...
```

> [!TIP]
> Place your video files in separate directories for each camera view to maintain organization and enable proper synchronization.



