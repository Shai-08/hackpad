import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros

keyboard = KMKKeyboard()

# --- Define macros ---
macros = Macros()
macros.define_macro("HELLO", [KC.H, KC.E, KC.L, KC.L, KC.O])
keyboard.modules.append(macros)

# --- Matrix pins ---
# Four keys + encoder push
PINS = [board.GP1, board.GP2, board.GP4, board.GP29, board.GP14]  # last pin = encoder push

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False
)

# --- Encoder (rotary) ---
encoder_handler = EncoderHandler()
# Encoder A,B pins (replace with your pins)
encoder_handler.pins = [(board.GP28, board.GP0)]
# Map encoder rotation to (CW, CCW)
encoder_handler.map = [
    (KC.VOLU, KC.VOLD),
]
keyboard.modules.append(encoder_handler)

# --- Keymap ---
# Now 1x5 (4 keys + encoder push). Encoder push is the last key (mapped to KC.MUTE).
keyboard.keymap = [
    [KC.A, KC.DELETE, KC.MACRO("HELLO"), KC.ENTER, KC.MUTE],
]

if __name__ == "__main__":
    keyboard.go()
