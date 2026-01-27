# Hand-Controlled Desktop UI 🖐️

A computer vision-based desktop interface controlled entirely by hand gestures using your webcam. Built with Python, OpenCV, and MediaPipe.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/mediapipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

### 🎮 Interactive Desktop UI
- **Virtual Keyboard**: Full QWERTY keyboard with space, backspace, and enter keys
- **Web Browser Integration**: Open browser and perform Google searches
- **Ball Bounce Game**: Two-hand controlled game with physics-based ball bouncing
- **Camera Background**: Toggle between camera feed and solid background
- **Hand Tracking Visualization**: Toggle hand skeleton overlay on/off

### 🎯 Gesture Controls
- **Cursor Control**: Move your index finger to control the cursor
- **Click Gesture**: Pinch thumb and index finger together to click
- **Two-Hand Bar**: In game mode, both hands create a bar between palms

### 🎲 Ball Bounce Game
- 60-second gameplay with 20 balls
- Score points by bouncing balls with the bar created between your hands
- Combo system for consecutive bounces
- Real-time stats display (score, combo, time, balls remaining)
- Game over screen with final statistics

## Demo

https://github.com/user-attachments/assets/your-demo-video.mp4

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (internal or external)
- Windows, macOS, or Linux

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rikiza89/Mirror_Screen_prototype.git
cd hand-controlled-desktop-ui
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python hand_ui_prototype.py
```

### Controls

#### Main UI Mode
- **Move cursor**: Point your index finger at the camera
- **Click**: Pinch thumb and index finger together
- **Keyboard button**: Toggle virtual keyboard visibility
- **Browser button**: Open default web browser
- **Search button**: Search Google with typed text
- **Ball Game button**: Start the ball bounce game
- **Camera BG button**: Toggle camera background on/off
- **Show Hands button**: Toggle hand landmarks visualization on/off

#### Game Mode
- **Show both hands**: Create a bar between your palms
- **Move hands**: Position the bar to bounce falling balls
- **Avoid missing**: Missing balls resets your combo
- **Time limit**: 60 seconds to score as many points as possible

### Keyboard Shortcuts
- **Q**: Quit application
- **X button**: Close window

## Configuration

You can adjust these parameters in the code:

```python
# UI Configuration
UI_WIDTH = 1280
UI_HEIGHT = 720
PINCH_THRESHOLD = 40  # Adjust for hand size

# Game Configuration
GAME_DURATION = 60  # seconds
TOTAL_BALLS = 20
BALL_SPEED = 5
BAR_THICKNESS = 20
```

## Troubleshooting

### Cursor not moving
- Ensure good lighting conditions
- Check webcam permissions
- Adjust `PINCH_THRESHOLD` if pinch detection is too sensitive/insensitive

### Hand detection issues
- Position yourself 1-2 feet from camera
- Ensure hands are clearly visible
- Avoid cluttered backgrounds
- Toggle "Show Hands" to debug hand tracking

### Performance issues
- Close other applications using the webcam
- Reduce `UI_WIDTH` and `UI_HEIGHT` for better FPS
- Ensure adequate CPU resources

### Camera not found
- Check webcam connection
- Verify camera permissions
- Try changing camera index in code: `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

## Technical Details

### Hand Tracking
- **MediaPipe Hands**: 21 hand landmarks per hand
- **Palm Detection**: Average of wrist and finger base landmarks
- **Gesture Recognition**: Distance-based pinch detection

### Coordinate Mapping
- Camera space → UI space conversion
- Horizontal flip for mirror effect
- Real-time cursor position tracking

### Game Physics
- Constant velocity ball movement
- Wall collision detection
- Bar-ball intersection testing
- Combo tracking system

## Project Structure

```
hand-controlled-desktop-ui/
├── hand_ui_prototype.py    # Main application
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── LICENSE                 # MIT License
```

## Dependencies

- **OpenCV**: Video capture and image processing
- **MediaPipe**: Hand tracking and landmark detection
- **NumPy**: Numerical operations
- **webbrowser**: Browser integration (standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Multi-gesture support (swipe, rotate, zoom)
- [ ] Customizable UI themes
- [ ] Additional mini-games
- [ ] Voice command integration
- [ ] Multi-user support
- [ ] Gesture recording and playback
- [ ] Settings menu for easier configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking solution
- [OpenCV](https://opencv.org/) for computer vision tools
- Inspired by gesture-based interaction research

## Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [(https://github.com/Rikiza89/Mirror_Screen_prototype)](https://github.com/Rikiza89/Mirror_Screen_prototype)

---

⭐ Star this repository if you find it helpful!
