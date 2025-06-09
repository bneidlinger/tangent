# pipboy_log_display.py
import pygame
import threading
import random
import time
import os

# --- CONFIG ---
LOG_FILE = "C:/Windows/System32/LogFiles/WMI/RtBackup/EtwRTDiagLog.etl"  # Change this to your log file
MAX_LINES = 20
FONT_SIZE = 18
WINDOW_SIZE = (800, 480)
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (50, 255, 50)  # Fallout green
FLICKER_CHANCE = 0.05
FLICKER_INTENSITY = 60
FONT_NAME = "monospace"  # Try "monofonto" if available

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("PipBoy Console")
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
clock = pygame.time.Clock()

log_lines = []

def follow_log(file_path, callback):
    def reader():
        try:
            with open(file_path, 'r', errors='ignore') as f:
                f.seek(0, os.SEEK_END)  # Go to the end of the file
                while True:
                    line = f.readline()
                    if line:
                        callback(line.strip())
                    else:
                        time.sleep(0.1)
        except Exception as e:
            callback(f"[ERROR] {e}")

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

def add_log_line(line):
    if len(log_lines) >= MAX_LINES:
        log_lines.pop(0)
    log_lines.append(line)

# --- Start log follower ---
follow_log(LOG_FILE, add_log_line)

# --- Main Loop ---
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for idx, line in enumerate(log_lines):
        flicker = random.randint(-FLICKER_INTENSITY, FLICKER_INTENSITY) if random.random() < FLICKER_CHANCE else 0
        flicker_color = (
            max(min(TEXT_COLOR[0] + flicker, 255), 0),
            max(min(TEXT_COLOR[1] + flicker, 255), 0),
            max(min(TEXT_COLOR[2] + flicker, 255), 0)
        )
        text_surface = font.render(line, True, flicker_color)
        screen.blit(text_surface, (10, 10 + idx * (FONT_SIZE + 2)))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

# --- requirements.txt generator ---
# Run this separately to create requirements.txt if needed
if __name__ == "__main__":
    with open("requirements.txt", "w") as f:
        f.write("pygame\n")
    print("requirements.txt created.")
