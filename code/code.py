import time
import board
import digitalio
import usb_hid

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# -----------------------------
# Rotary Encoder Pins
# -----------------------------
clk = digitalio.DigitalInOut(board.GP26)
clk.switch_to_input(pull=digitalio.Pull.UP)

dt = digitalio.DigitalInOut(board.GP27)
dt.switch_to_input(pull=digitalio.Pull.UP)

# Encoder button → Play/Pause
enc_button = digitalio.DigitalInOut(board.GP28)
enc_button.switch_to_input(pull=digitalio.Pull.UP)

# Button 1 → Mute toggle
mute_button = digitalio.DigitalInOut(board.GP1)
mute_button.switch_to_input(pull=digitalio.Pull.UP)

# Button 3 → Previous Track (double‑tap)
prev_button = digitalio.DigitalInOut(board.GP3)
prev_button.switch_to_input(pull=digitalio.Pull.UP)

# Button 4 → Next Track (double‑tap)
next_button = digitalio.DigitalInOut(board.GP4)
next_button.switch_to_input(pull=digitalio.Pull.UP)

# HID consumer control
cc = ConsumerControl(usb_hid.devices)

# -----------------------------
# State Tracking
# -----------------------------
last_clk = clk.value
last_enc_btn = enc_button.value
last_mute_btn = mute_button.value
last_prev_btn = prev_button.value
last_next_btn = next_button.value

debounce_time = 0.15
double_tap_window = 1.0  # 1 second

last_enc_press = 0
last_mute_press = 0
last_prev_press = 0
last_next_press = 0

prev_first_tap = 0
next_first_tap = 0

is_muted = False

print("Media controller ready.")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    now = time.monotonic()

    # -------------------------
    # Rotary Encoder Rotation (FLIPPED)
    # -------------------------
    current_clk = clk.value

    if last_clk and not current_clk:
        if dt.value:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            print("Volume Down")
        else:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            print("Volume Up")

    last_clk = current_clk

    # -------------------------
    # Encoder Button → Play/Pause
    # -------------------------
    enc_val = enc_button.value
    if last_enc_btn and not enc_val:
        if now - last_enc_press > debounce_time:
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            print("Play/Pause")
            last_enc_press = now
    last_enc_btn = enc_val

    # -------------------------
    # Button 1 → Toggle Mute
    # -------------------------
    mute_val = mute_button.value
    if last_mute_btn and not mute_val:
        if now - last_mute_press > debounce_time:
            cc.send(ConsumerControlCode.MUTE)
            is_muted = not is_muted
            print("Muted" if is_muted else "Unmuted")
            last_mute_press = now
    last_mute_btn = mute_val

    # -------------------------
    # Button 3 → Previous Track (double‑tap)
    # -------------------------
    prev_val = prev_button.value
    if last_prev_btn and not prev_val:
        if now - last_prev_press > debounce_time:
            if now - prev_first_tap < double_tap_window:
                cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
                print("Previous Track (double‑tap)")
                prev_first_tap = 0
            else:
                prev_first_tap = now
            last_prev_press = now
    last_prev_btn = prev_val

    # -------------------------
    # Button 4 → Next Track (double‑tap)
    # -------------------------
    next_val = next_button.value
    if last_next_btn and not next_val:
        if now - last_next_press > debounce_time:
            if now - next_first_tap < double_tap_window:
                cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
                print("Next Track (double‑tap)")
                next_first_tap = 0
            else:
                next_first_tap = now
            last_next_press = now
    last_next_btn = next_val

    time.sleep(0.001)
