############################################
# Reference USB HID keycodes at
# https://circuitpython.readthedocs.io/projects/hid/en/latest/
#
# Escape character  Prints as
#       \'           Single quote
#       \"           Double quote
#       \t           Tab
#       \n           Newline (line break)
#       \\           Backslash
############################################

from adafruit_hid.keycode import Keycode
groups = {}
############################################
# Begin group 0
############################################
codes = {}
codes[1]={}
codes[2]={}
codes[3]={}
codes[4]={}
codes[5]={}
codes[6]={}
codes[7]={}
codes[8]={}

# codes to channe groups
codes[5][0b00010] = "group 1"
codes[8][0b00001111] = "group 2"

#letters
codes[2][0b01]='a'
codes[4][0b1000]='b'
#codes[4][0b1010]='c'   # standard morse c
codes[4][0b1110]='c'
codes[3][0b100]='d'
codes[1][0b0]='e'
codes[4][0b0010]='f'
codes[3][0b110]='g'
codes[4][0b0000]='h'
codes[2][0b00]='i'
codes[4][0b0111]='j'
codes[3][0b101]='k'
codes[4][0b0100]='l'
#codes[2][0b11]='m'     # standard morse m
codes[4][0b1111]='m'
codes[2][0b10]='n'
codes[3][0b111]='o'
codes[4][0b0110]='p'
codes[4][0b1101]='q'
codes[3][0b010]='r'
codes[3][0b000]='s'
codes[1][0b1]='t'
codes[3][0b001]='u'
codes[4][0b0001]='v'
codes[3][0b011]='w'
codes[4][0b1001]='x'
codes[4][0b1011]='y'
codes[4][0b1100]='z'
#Numbers
codes[5][0b01111]='1'
codes[5][0b00111]='2'
codes[5][0b00011]='3'
codes[5][0b00001]='4'
codes[5][0b00000]='5'
codes[5][0b10000]='6'
codes[5][0b11000]='7'
codes[5][0b11100]='8'
codes[5][0b11110]='9'
codes[5][0b11111]='0'
#punctuation
codes[5][0b10001]='+'
codes[5][0b01110]='-'
codes[5][0b11101]='='
codes[5][0b10011]='*'
codes[6][0b010000]='!'
codes[6][0b111001]='@'
codes[6][0b001110]='#'
codes[6][0b001111]='$'
codes[6][0b000101]='%'
codes[6][0b100011]='^'
codes[6][0b011100]='&'
codes[6][0b011111]='.'
codes[6][0b100000]=','
codes[6][0b011110]=':'
codes[6][0b100001]=';'
codes[6][0b000111]=')'
codes[6][0b111000]='('
codes[6][0b100111]=']'
codes[6][0b011000]='['
codes[5][0b11001]='}'
codes[5][0b00110]='{'
codes[6][0b110011]='<'
codes[6][0b001100]='>'
codes[6][0b101111]='?'
codes[6][0b000011]='/'  # forward_slash
codes[6][0b111100]='\\' # backslash
codes[6][0b000010]='|'
codes[6][0b111101]='_'
codes[6][0b000110]='\"' # double-quote
codes[6][0b001000]='\'' # single-quote
codes[6][0b110111]='`'  # grave_accent
codes[6][0b111011]='~'
codes[5][0b01001]=Keycode.UP_ARROW     # au
codes[5][0b01100]=Keycode.DOWN_ARROW   # ad
codes[6][0b010100]=Keycode.LEFT_ARROW  # al
codes[5][0b01101]=Keycode.RIGHT_ARROW  # ar
codes[7][0b0000000]=Keycode.HOME
codes[7][0b0001000]=Keycode.END
codes[6][0b000001]=Keycode.PAGE_UP
codes[6][0b000100]=Keycode.PAGE_DOWN
codes[4][0b0101]=Keycode.ENTER
codes[6][0b110000]=Keycode.ESCAPE
codes[6][0b101100]=Keycode.DELETE
codes[5][0b10100]=Keycode.INSERT
codes[2][0b11]=Keycode.BACKSPACE        # code for stardard morse m
codes[4][0b0011]=Keycode.SPACE
codes[7][0b1110010]=Keycode.TAB

codes[6][0b111110]=Keycode.CAPS_LOCK
codes[6][0b110100]=Keycode.SCROLL_LOCK
codes[7][0b1110001]=Keycode.KEYPAD_NUMLOCK
codes[6][0b110110]=Keycode.PRINT_SCREEN
codes[7][0b1101111]=Keycode.F1
codes[7][0b1100111]=Keycode.F2
codes[7][0b1100011]=Keycode.F3
codes[7][0b1100001]=Keycode.F4
codes[7][0b1100000]=Keycode.F5
codes[7][0b1110000]=Keycode.F6
codes[7][0b1111000]=Keycode.F7
codes[7][0b1111100]=Keycode.F8
codes[7][0b1111110]=Keycode.F9
codes[7][0b1111111]=Keycode.F10
codes[7][0b0111111]=Keycode.F11
codes[7][0b0011111]=Keycode.F12

# modifer keys
codes[4][0b1010]=Keycode.LEFT_CONTROL   # code for standard morse c
codes[6][0b110001]=Keycode.LEFT_SHIFT   # LEFT_ALT also known as Option (Mac)
codes[5][0b11011]=Keycode.LEFT_ALT      # LEFT_GUI also known as the Windows key, Command (Mac), or Meta
codes[6][0b011011]=Keycode.LEFT_GUI     # windows key ww

############################################
# End group 0
groups[0]=codes
############################################

############################################
# Begin group 1 - Mouse, Numpad, Windows shortcuts
############################################
winCodes = {}
winCodes[1]={}
winCodes[2]={}
winCodes[3]={}
winCodes[4]={}
winCodes[5]={}
winCodes[6]={}
winCodes[7]={}
winCodes[8]={}

# codes to change groups
winCodes[5][0b00010] = "group 2"
winCodes[8][0b00000000] = "group 0"

# mouseMove x y wheel
#
#Parameters
# x – Move the mouse along the x axis. Negative is to the left, positive is to the right.
# y – Move the mouse along the y axis. Negative is upwards on the display, positive is downwards.
# wheel – Rotate the wheel this amount. Negative is toward the user, positive is away from the user.
#
winCodes[1][0b1] = "mmove 0 -1 0"   # mouse move up
winCodes[2][0b11] = "mmove 0 1 0"   # mouse move down
winCodes[3][0b000] = "mmove 1 0 0"  # mouse move right
winCodes[2][0b00] = "mmove -1 0 0"  # mouse move left
winCodes[6][0b000001] = "mmove 0 0 1"    # mouse wheel up
winCodes[6][0b000100] = "mmove 0 0 -1"   # mouse wheel down

winCodes[1][0b0] = "mrepeat"
winCodes[4][0b1100] = "mslow"
winCodes[5][0b00111] = "mfast"

# mouse buttons
winCodes[2][0b01] = "mclick left 1"     # left button single click
winCodes[3][0b011] = "mclick right 1"   # right button single click
winCodes[3][0b001] = "mclick left 2"    # left button double click
winCodes[4][0b0011] = "mclick right 2"  # right button double click


#Keypad Numbers
#winCodes[5][0b01111]=Keycode.KEYPAD_ONE
#winCodes[5][0b00111]=Keycode.KEYPAD_TWO
#winCodes[5][0b00011]=Keycode.KEYPAD_THREE
#winCodes[5][0b00001]=Keycode.KEYPAD_FOUR
#winCodes[5][0b00000]=Keycode.KEYPAD_FIVE
#winCodes[5][0b10000]=Keycode.KEYPAD_SIX
#winCodes[5][0b11000]=Keycode.KEYPAD_SEVEN
#winCodes[5][0b11100]=Keycode.KEYPAD_EIGHT
#winCodes[5][0b11110]=Keycode.KEYPAD_NINE
#winCodes[5][0b11111]=Keycode.KEYPAD_ZERO

#winCodes[5][0b10001]=Keycode.KEYPAD_PLUS
#winCodes[5][0b01110]=Keycode.KEYPAD_MINUS
#winCodes[5][0b11101]=Keycode.KEYPAD_EQUALS
#winCodes[5][0b10011]=Keycode.KEYPAD_ASTERISK
#winCodes[6][0b011111]=Keycode.KEYPAD_PERIOD
#winCodes[6][0b000011]=Keycode.KEYPAD_FORWARD_SLASH
#winCodes[6][0b111100]=Keycode.KEYPAD_BACKSLASH
#winCodes[7][0b1110001]=Keycode.KEYPAD_NUMLOCK
winCodes[4][0b0101]=Keycode.KEYPAD_ENTER
winCodes[5][0b01001]=Keycode.UP_ARROW     # au
winCodes[5][0b01100]=Keycode.DOWN_ARROW   # ad
winCodes[6][0b010100]=Keycode.LEFT_ARROW  # al
winCodes[5][0b01101]=Keycode.RIGHT_ARROW  # ar

#Releases mouse and keyboard focus from the Virtual Machine Connection window.
#	CTRL + ALT + LEFT ARROW
winCodes[6][0b110000]=Keycode.RIGHT_CONTROL, Keycode.RIGHT_ALT, Keycode.LEFT_ARROW

#	Switches between programs from left to right
winCodes[7][0b1111111]=Keycode.ALT, Keycode.TAB

#  Cycles through the programs in the order they were started
winCodes[7][0b0000000]=Keycode.ALT, Keycode.ESCAPE

# modifer keys
winCodes[4][0b1010]=Keycode.RIGHT_CONTROL
winCodes[6][0b110001]=Keycode.RIGHT_SHIFT
winCodes[5][0b11011]=Keycode.RIGHT_ALT
winCodes[6][0b011011]=Keycode.RIGHT_GUI
############################################
# End group 1
groups[1]=winCodes
############################################

############################################
# Begin group 2 - Shortcuts
############################################
shortCuts = {}
shortCuts[1]={}
shortCuts[2]={}
shortCuts[3]={}
shortCuts[4]={}
shortCuts[5]={}
shortCuts[6]={}
shortCuts[7]={}
shortCuts[8]={}

# codes to change to group 0
shortCuts[5][0b00010] = "group 0"
shortCuts[8][0b00000000] = "group 0"

#letters
shortCuts[2][0b01]='John Smith'
shortCuts[4][0b1000]='b'
shortCuts[4][0b1110]='c'
shortCuts[3][0b100]='d'
shortCuts[1][0b0]='username@domain.com\n'
shortCuts[4][0b0010]='f'
shortCuts[3][0b110]='g'
shortCuts[4][0b0000]='\'hello\''
shortCuts[2][0b00]='i'
shortCuts[4][0b0111]='j'
shortCuts[3][0b101]='k'
shortCuts[4][0b0100]='l'
shortCuts[4][0b1111]='m'
shortCuts[2][0b10]='n'
shortCuts[3][0b111]='o'
shortCuts[4][0b0110]='p'
shortCuts[4][0b1101]='q'
shortCuts[3][0b010]='r'
shortCuts[3][0b000]='s'
shortCuts[1][0b1]='t'
shortCuts[3][0b001]='u'
shortCuts[4][0b0001]='v'
shortCuts[3][0b011]='w'
shortCuts[4][0b1001]='x'
shortCuts[4][0b1011]='y'
shortCuts[4][0b1100]='z'
#Numbers
shortCuts[5][0b01111]='password1'
shortCuts[5][0b00111]='password2'
shortCuts[5][0b00011]='password3'
shortCuts[5][0b00001]='4'
shortCuts[5][0b00000]='5'
shortCuts[5][0b10000]='6'
shortCuts[5][0b11000]='7'
shortCuts[5][0b11100]='8'
shortCuts[5][0b11110]='9'
shortCuts[5][0b11111]='0'

shortCuts[4][0b0101]=Keycode.ENTER
shortCuts[2][0b11]=Keycode.BACKSPACE 
############################################
# End group 2
groups[2]=shortCuts
############################################