"""
Hand-Controlled Desktop UI Prototype
Uses webcam + MediaPipe to control a virtual desktop interface with hand gestures
Includes: Ball Bounce Game with Camera Background!
"""

import cv2
import mediapipe as mp
import numpy as np
import webbrowser
import time
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Changed to 2 for game
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# UI Configuration
UI_WIDTH = 1280
UI_HEIGHT = 720
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
KEY_SIZE = 60
KEY_MARGIN = 10

# Colors (BGR)
COLOR_BG = (40, 40, 40)
COLOR_BUTTON = (70, 70, 70)
COLOR_BUTTON_HOVER = (100, 100, 150)
COLOR_BUTTON_CLICK = (150, 200, 150)
COLOR_CURSOR = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_KEYBOARD_BG = (50, 50, 50)
COLOR_KEY = (80, 80, 80)
COLOR_KEY_HOVER = (120, 120, 180)

# Game Configuration
GAME_DURATION = 60  # seconds
TOTAL_BALLS = 20
BALL_RADIUS = 15
BALL_SPEED = 5
BAR_THICKNESS = 20
BALL_SPAWN_INTERVAL = GAME_DURATION / TOTAL_BALLS  # Evenly distribute spawns

# Pinch detection threshold
PINCH_THRESHOLD = 40  # pixels

# Ball class for game
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)  # Random horizontal velocity
        self.vy = BALL_SPEED  # Constant downward velocity
        self.radius = BALL_RADIUS
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.active = True
    
    def update(self):
        """Update ball position"""
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off side walls
        if self.x - self.radius <= 0 or self.x + self.radius >= UI_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(UI_WIDTH - self.radius, self.x))
        
        # Check if ball fell off screen
        if self.y - self.radius > UI_HEIGHT:
            self.active = False
    
    def bounce_off_bar(self):
        """Reverse vertical velocity when bouncing off bar"""
        self.vy = -abs(self.vy)  # Always bounce upward
        # Add slight horizontal variation for fun
        self.vx += random.uniform(-1, 1)
        self.vx = max(-8, min(8, self.vx))  # Limit horizontal speed
    
    def draw(self, frame):
        """Draw the ball"""
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, self.color, -1)
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, (255, 255, 255), 2)


# Game State class
class GameState:
    def __init__(self):
        self.active = False
        self.game_over = False
        self.balls = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.start_time = 0
        self.last_spawn_time = 0
        self.balls_spawned = 0
        self.bar_pos = None  # (x1, y1, x2, y2)
    
    def start_game(self):
        """Initialize a new game"""
        self.active = True
        self.game_over = False
        self.balls = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.start_time = time.time()
        self.last_spawn_time = time.time()
        self.balls_spawned = 0
        self.bar_pos = None
    
    def reset_game(self):
        """Reset to main menu"""
        self.active = False
        self.game_over = False
        self.balls = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.balls_spawned = 0
        self.bar_pos = None
    
    def update(self, bar_pos):
        """Update game state"""
        if not self.active or self.game_over:
            return
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Check if game should end
        if elapsed >= GAME_DURATION:
            self.end_game()
            return
        
        # Spawn new balls
        if (self.balls_spawned < TOTAL_BALLS and 
            current_time - self.last_spawn_time >= BALL_SPAWN_INTERVAL):
            self.spawn_ball()
            self.last_spawn_time = current_time
        
        # Update bar position
        self.bar_pos = bar_pos
        
        # Update all balls
        combo_broken = False
        for ball in self.balls:
            if ball.active:
                ball.update()
                
                # Check collision with bar
                if bar_pos and self.check_bar_collision(ball, bar_pos):
                    ball.bounce_off_bar()
                    self.score += 1
                    self.combo += 1
                    self.max_combo = max(self.max_combo, self.combo)
        
        # Remove inactive balls
        self.balls = [b for b in self.balls if b.active]
        
        # Check if all balls are gone and no more to spawn
        if len(self.balls) == 0 and self.balls_spawned >= TOTAL_BALLS:
            self.end_game()
    
    def spawn_ball(self):
        """Spawn a new ball at random x position at top"""
        x = random.randint(BALL_RADIUS + 50, UI_WIDTH - BALL_RADIUS - 50)
        y = -BALL_RADIUS  # Start above screen
        self.balls.append(Ball(x, y))
        self.balls_spawned += 1
    
    def check_bar_collision(self, ball, bar_pos):
        """Check if ball collides with bar"""
        x1, y1, x2, y2 = bar_pos
        
        # Check if ball is near bar vertically
        if abs(ball.y - y1) > BALL_RADIUS + BAR_THICKNESS:
            return False
        
        # Check if ball is within bar horizontally (with some tolerance)
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        
        # Check if ball center is within bar range
        if min_x - BALL_RADIUS <= ball.x <= max_x + BALL_RADIUS:
            # Check if ball is moving downward
            if ball.vy > 0:
                return True
        
        return False
    
    def end_game(self):
        """End the game"""
        self.game_over = True
    
    def get_time_remaining(self):
        """Get remaining time in seconds"""
        if not self.active:
            return 0
        elapsed = time.time() - self.start_time
        return max(0, GAME_DURATION - elapsed)


# Button class for ROI management
class Button:
    def __init__(self, x, y, w, h, label, action):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.action = action
        self.is_hovered = False
        self.click_time = 0
    
    def contains(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h
    
    def draw(self, frame):
        current_time = time.time()
        # Flash effect on click
        if current_time - self.click_time < 0.2:
            color = COLOR_BUTTON_CLICK
        elif self.is_hovered:
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON
        
        cv2.rectangle(frame, (self.x, self.y), 
                     (self.x + self.w, self.y + self.h), color, -1)
        cv2.rectangle(frame, (self.x, self.y), 
                     (self.x + self.w, self.y + self.h), (200, 200, 200), 2)
        
        # Center text
        text_size = cv2.getTextSize(self.label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        text_x = self.x + (self.w - text_size[0]) // 2
        text_y = self.y + (self.h + text_size[1]) // 2
        cv2.putText(frame, self.label, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 2)
    
    def click(self):
        self.click_time = time.time()
        if self.action:
            self.action()


# Application state
class AppState:
    def __init__(self):
        self.keyboard_visible = False
        self.typed_text = ""
        self.last_click_time = 0
        self.click_cooldown = 0.3  # seconds
        self.show_camera_bg = True  # Toggle for camera background
        self.show_hand_landmarks = True  # Toggle for hand detection visualization
    
    def toggle_keyboard(self):
        self.keyboard_visible = not self.keyboard_visible
    
    def toggle_camera_bg(self):
        self.show_camera_bg = not self.show_camera_bg
    
    def toggle_landmarks(self):
        self.show_hand_landmarks = not self.show_hand_landmarks
    
    def type_char(self, char):
        if char == "BACK":
            self.typed_text = self.typed_text[:-1]
        elif char == "SPACE":
            self.typed_text += " "
        elif char == "ENTER":
            self.typed_text += "\n"
        else:
            self.typed_text += char
    
    def open_browser(self):
        webbrowser.open("https://www.google.com")
    
    def google_search(self):
        if self.typed_text.strip():
            query = self.typed_text.strip().replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    
    def can_click(self):
        current_time = time.time()
        if current_time - self.last_click_time > self.click_cooldown:
            self.last_click_time = current_time
            return True
        return False


# Initialize app state and game state
state = AppState()
game = GameState()

# Create main buttons - adjusted for more buttons
buttons = []
button_y = BUTTON_MARGIN
button_width = 130

buttons.append(Button(BUTTON_MARGIN, button_y, button_width, BUTTON_HEIGHT,
                     "Keyboard", state.toggle_keyboard))
buttons.append(Button(BUTTON_MARGIN + (button_width + 10) * 1, button_y, button_width, 
                     BUTTON_HEIGHT, "Browser", state.open_browser))
buttons.append(Button(BUTTON_MARGIN + (button_width + 10) * 2, button_y, button_width,
                     BUTTON_HEIGHT, "Search", state.google_search))
buttons.append(Button(BUTTON_MARGIN + (button_width + 10) * 3, button_y, button_width,
                     BUTTON_HEIGHT, "Ball Game", game.start_game))
buttons.append(Button(BUTTON_MARGIN + (button_width + 10) * 4, button_y, button_width,
                     BUTTON_HEIGHT, "Camera BG", state.toggle_camera_bg))
buttons.append(Button(BUTTON_MARGIN + (button_width + 10) * 5, button_y, button_width,
                     BUTTON_HEIGHT, "Show Hands", state.toggle_landmarks))

# Keyboard layout
keyboard_keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['SPACE', 'BACK', 'ENTER']
]

def create_keyboard_buttons():
    """Create keyboard button objects dynamically"""
    kb_buttons = []
    start_y = 200
    
    for row_idx, row in enumerate(keyboard_keys):
        row_width = len(row) * (KEY_SIZE + KEY_MARGIN)
        start_x = (UI_WIDTH - row_width) // 2
        
        for col_idx, key in enumerate(row):
            x = start_x + col_idx * (KEY_SIZE + KEY_MARGIN)
            y = start_y + row_idx * (KEY_SIZE + KEY_MARGIN)
            
            # Special width for space, back, enter
            if key in ['SPACE', 'BACK', 'ENTER']:
                w = KEY_SIZE * 2
            else:
                w = KEY_SIZE
            
            kb_buttons.append(Button(x, y, w, KEY_SIZE - 5, key,
                                    lambda k=key: state.type_char(k)))
    
    return kb_buttons


def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def detect_pinch(hand_landmarks, frame_width, frame_height):
    """Detect thumb-index pinch gesture"""
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    
    thumb_px = (int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height))
    index_px = (int(index_tip.x * frame_width), int(index_tip.y * frame_height))
    
    distance = calculate_distance(thumb_px, index_px)
    return distance < PINCH_THRESHOLD, distance


def map_to_ui(x, y, cam_width, cam_height):
    """Map camera coordinates to UI coordinates (with flip for mirror effect)"""
    ui_x = int(x * UI_WIDTH)  # Remove flip
    # ui_x = int((1 - x) * UI_WIDTH)  # Flip horizontally for mirror effect
    ui_y = int(y * UI_HEIGHT)
    return np.clip(ui_x, 0, UI_WIDTH - 1), np.clip(ui_y, 0, UI_HEIGHT - 1)


def get_palm_center(hand_landmarks, cam_width, cam_height):
    """Get palm center position (average of wrist and base knuckles)"""
    # Use landmarks 0 (wrist), 5, 9, 13, 17 (base of each finger)
    palm_points = [0, 5, 9, 13, 17]
    x_sum = 0
    y_sum = 0
    
    for idx in palm_points:
        landmark = hand_landmarks.landmark[idx]
        x_sum += landmark.x
        y_sum += landmark.y
    
    avg_x = x_sum / len(palm_points)
    avg_y = y_sum / len(palm_points)
    
    return map_to_ui(avg_x, avg_y, cam_width, cam_height)


def draw_game_ui(frame, cursor_pos, fps, cam_frame, hand_landmarks_list):
    """Draw the game UI"""
    # Background - camera or dark
    if state.show_camera_bg and cam_frame is not None:
        # Resize camera frame to UI size
        bg = cv2.resize(cam_frame, (UI_WIDTH, UI_HEIGHT))
        # Flip horizontally for mirror effect
        bg = cv2.flip(bg, 1)
        # Darken slightly for better visibility of game elements
        bg = cv2.addWeighted(bg, 0.6, np.zeros_like(bg), 0.4, 0)
        frame[:] = bg
    else:
        frame[:] = (20, 20, 20)
    
    # Draw all balls
    for ball in game.balls:
        ball.draw(frame)
    
    # Draw bar if two hands detected
    if game.bar_pos:
        x1, y1, x2, y2 = game.bar_pos
        # Draw bar with gradient effect
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), BAR_THICKNESS)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)
        
        # Draw palm indicators
        cv2.circle(frame, (x1, y1), 15, (0, 200, 255), -1)
        cv2.circle(frame, (x2, y2), 15, (0, 200, 255), -1)
    
    # Draw game HUD
    time_remaining = game.get_time_remaining()
    
    # Top bar with stats
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (UI_WIDTH, 80), (40, 40, 40), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Score
    cv2.putText(frame, f"SCORE: {game.score}", (20, 50),
               cv2.FONT_HERSHEY_BOLD, 1.2, (0, 255, 0), 3)
    
    # Combo
    combo_color = (0, 255, 255) if game.combo > 0 else (100, 100, 100)
    cv2.putText(frame, f"COMBO: {game.combo}x", (350, 50),
               cv2.FONT_HERSHEY_BOLD, 1.2, combo_color, 3)
    
    # Time
    time_color = (0, 255, 0) if time_remaining > 10 else (0, 0, 255)
    cv2.putText(frame, f"TIME: {int(time_remaining)}s", (700, 50),
               cv2.FONT_HERSHEY_BOLD, 1.2, time_color, 3)
    
    # Balls remaining
    balls_left = TOTAL_BALLS - game.balls_spawned + len(game.balls)
    cv2.putText(frame, f"BALLS: {balls_left}", (1000, 50),
               cv2.FONT_HERSHEY_BOLD, 1.2, (255, 200, 0), 3)
    
    # Instructions if no bar detected
    if not game.bar_pos:
        cv2.putText(frame, "SHOW BOTH HANDS TO CREATE BAR!", (UI_WIDTH//2 - 300, UI_HEIGHT//2),
                   cv2.FONT_HERSHEY_BOLD, 1.0, (0, 0, 255), 2)


def draw_game_over_ui(frame):
    """Draw game over screen"""
    # Semi-transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (UI_WIDTH, UI_HEIGHT), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Game Over text
    cv2.putText(frame, "GAME OVER!", (UI_WIDTH//2 - 200, 150),
               cv2.FONT_HERSHEY_BOLD, 2.0, (0, 0, 255), 4)
    
    # Stats
    y_offset = 280
    cv2.putText(frame, f"Final Score: {game.score}", (UI_WIDTH//2 - 150, y_offset),
               cv2.FONT_HERSHEY_BOLD, 1.5, (0, 255, 0), 3)
    
    cv2.putText(frame, f"Max Combo: {game.max_combo}x", (UI_WIDTH//2 - 150, y_offset + 80),
               cv2.FONT_HERSHEY_BOLD, 1.5, (0, 255, 255), 3)
    
    # Buttons
    play_again_btn = Button(UI_WIDTH//2 - 250, 450, 200, 60, "Play Again", game.start_game)
    exit_btn = Button(UI_WIDTH//2 + 50, 450, 200, 60, "Exit to Menu", game.reset_game)
    
    play_again_btn.draw(frame)
    exit_btn.draw(frame)
    
    return [play_again_btn, exit_btn]


def draw_ui(frame, cursor_pos, pinch_detected, pinch_distance, fps, cam_frame, hand_landmarks_list):
    """Draw the complete UI"""
    # Background - camera or solid color
    if state.show_camera_bg and cam_frame is not None:
        # Resize camera frame to UI size
        bg = cv2.resize(cam_frame, (UI_WIDTH, UI_HEIGHT))
        # Flip horizontally for mirror effect
        bg = cv2.flip(bg, 1)
        # Darken for better UI visibility
        bg = cv2.addWeighted(bg, 0.5, np.zeros_like(bg), 0.5, 0)
        frame[:] = bg
    else:
        frame[:] = COLOR_BG
    
    # Title bar with semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (UI_WIDTH, 80), (60, 60, 60), -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    
    cv2.putText(frame, "HAND-CONTROLLED DESKTOP UI", (20, 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, COLOR_TEXT, 2)
    
    # Main buttons
    for btn in buttons:
        btn.draw(frame)
    
    # Text input display
    input_y = button_y + BUTTON_HEIGHT + BUTTON_MARGIN
    overlay = frame.copy()
    cv2.rectangle(overlay, (BUTTON_MARGIN, input_y),
                 (UI_WIDTH - BUTTON_MARGIN, input_y + 60), (60, 60, 60), -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    cv2.rectangle(frame, (BUTTON_MARGIN, input_y),
                 (UI_WIDTH - BUTTON_MARGIN, input_y + 60), (150, 150, 150), 2)
    
    cv2.putText(frame, "Text Input:", (BUTTON_MARGIN + 10, input_y + 25),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    
    # Display typed text (truncate if too long)
    display_text = state.typed_text[-60:] if len(state.typed_text) > 60 else state.typed_text
    cv2.putText(frame, display_text, (BUTTON_MARGIN + 10, input_y + 50),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_TEXT, 2)
    
    # Virtual keyboard (if visible)
    if state.keyboard_visible:
        kb_buttons = create_keyboard_buttons()
        for kb_btn in kb_buttons:
            kb_btn.is_hovered = kb_btn.contains(cursor_pos[0], cursor_pos[1]) if cursor_pos else False
            kb_btn.draw(frame)
    
    # Status bar
    status_y = UI_HEIGHT - 40
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, status_y), (UI_WIDTH, UI_HEIGHT), (50, 50, 50), -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    
    status_text = f"FPS: {fps:.1f} | Pinch: {'YES' if pinch_detected else 'NO'} ({pinch_distance:.1f}px)"
    if state.keyboard_visible:
        status_text += " | KB: ON"
    status_text += f" | CamBG: {'ON' if state.show_camera_bg else 'OFF'}"
    status_text += f" | Hands: {'ON' if state.show_hand_landmarks else 'OFF'}"
    
    cv2.putText(frame, status_text, (20, status_y + 25),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)


def main():
    """Main application loop"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    prev_time = time.time()
    prev_pinch = False
    
    print("Hand-Controlled Desktop UI Started")
    print("Controls:")
    print("- Move index finger to control cursor")
    print("- Pinch thumb and index finger to click")
    print("- Use BOTH HANDS in game to create the bar")
    print("- Toggle 'Camera BG' to show/hide camera background")
    print("- Toggle 'Show Hands' to show/hide hand landmarks")
    print("- Press 'q' to quit")
    
    while True:
        ret, cam_frame = cap.read()
        if not ret:
            break
        
        # Process frame with MediaPipe
        cam_frame_rgb = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(cam_frame_rgb)
        
        # Draw hand landmarks on camera frame if enabled
        if state.show_hand_landmarks and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    cam_frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        
        cursor_pos = None
        pinch_detected = False
        pinch_distance = 0
        bar_pos = None
        hand_landmarks_list = []
        
        # Hand detection and tracking
        if results.multi_hand_landmarks:
            cam_height, cam_width, _ = cam_frame.shape
            hand_landmarks_list = results.multi_hand_landmarks
            
            # For game: detect two hands and create bar
            if len(results.multi_hand_landmarks) == 2 and game.active and not game.game_over:
                palm1 = get_palm_center(results.multi_hand_landmarks[0], cam_width, cam_height)
                palm2 = get_palm_center(results.multi_hand_landmarks[1], cam_width, cam_height)
                bar_pos = (palm1[0], palm1[1], palm2[0], palm2[1])
            
            # For UI: use first hand for cursor
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Get index finger tip position (landmark 8)
            index_tip = hand_landmarks.landmark[8]
            cursor_pos = map_to_ui(index_tip.x, index_tip.y, cam_width, cam_height)
            
            # Detect pinch gesture
            pinch_detected, pinch_distance = detect_pinch(hand_landmarks, cam_width, cam_height)
            # Draw cursor on camera frame NOW
            cam_cursor_x = int((1 - cursor_pos[0] / UI_WIDTH) * cam_width)
            cam_cursor_y = int((cursor_pos[1] / UI_HEIGHT) * cam_height)
            cv2.circle(cam_frame, (cam_cursor_x, cam_cursor_y), 12, COLOR_CURSOR, -1)
            cv2.circle(cam_frame, (cam_cursor_x, cam_cursor_y), 14, (255, 255, 255), 2)
            if pinch_detected:
                cv2.circle(cam_frame, (cam_cursor_x, cam_cursor_y), 20, (0, 0, 255), 3)
                
            # Handle click (pinch start) - only in UI mode
            if pinch_detected and not prev_pinch and state.can_click():
                if not game.active:
                    # Check main buttons
                    for btn in buttons:
                        if btn.contains(cursor_pos[0], cursor_pos[1]):
                            btn.click()
                            break
                    
                    # Check keyboard buttons if visible
                    if state.keyboard_visible:
                        kb_buttons = create_keyboard_buttons()
                        for kb_btn in kb_buttons:
                            if kb_btn.contains(cursor_pos[0], cursor_pos[1]):
                                kb_btn.click()
                                break
                
                elif game.game_over:
                    # Handle game over buttons
                    temp_frame = np.zeros((UI_HEIGHT, UI_WIDTH, 3), dtype=np.uint8)
                    game_over_buttons = draw_game_over_ui(temp_frame)
                    for btn in game_over_buttons:
                        if btn.contains(cursor_pos[0], cursor_pos[1]):
                            btn.click()
                            break
            
            prev_pinch = pinch_detected
        else:
            # Reset pinch state if no hands detected
            prev_pinch = False
        
        # Update game state
        if game.active and not game.game_over:
            game.update(bar_pos)
        
        # Create UI frame
        ui_frame = np.zeros((UI_HEIGHT, UI_WIDTH, 3), dtype=np.uint8)
        
        # Draw appropriate UI
        if game.active and not game.game_over:
            draw_game_ui(ui_frame, cursor_pos, fps, cam_frame, hand_landmarks_list)
        elif game.game_over:
            draw_game_ui(ui_frame, cursor_pos, fps, cam_frame, hand_landmarks_list)  # Draw game state first
            game_over_buttons = draw_game_over_ui(ui_frame)
            # Update hover states for game over buttons
            for btn in game_over_buttons:
                btn.is_hovered = btn.contains(cursor_pos[0], cursor_pos[1]) if cursor_pos else False
                btn.draw(ui_frame)
            # Draw cursor on top
            if cursor_pos:
                cv2.circle(ui_frame, cursor_pos, 12, COLOR_CURSOR, -1)
                cv2.circle(ui_frame, cursor_pos, 14, (255, 255, 255), 2)
                if pinch_detected:
                    cv2.circle(ui_frame, cursor_pos, 20, (0, 0, 255), 3)
        else:
            # Update hover states
            for btn in buttons:
                btn.is_hovered = btn.contains(cursor_pos[0], cursor_pos[1]) if cursor_pos else False
            
            draw_ui(ui_frame, cursor_pos, pinch_detected, pinch_distance, fps, cam_frame, hand_landmarks_list)
        
        # Display
        cv2.imshow("Hand-Controlled Desktop UI", ui_frame)
        
        # Quit on 'q' or window close
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if cv2.getWindowProperty("Hand-Controlled Desktop UI", cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()
