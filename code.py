from adafruit_macropad import MacroPad
import patterns

ROWS = 4
COLS = 3

BTNS = []
macropad = MacroPad()
score = 0


def copyPattern(p):
    b = []
    for i in patterns.patterns[p]:
        b.append(i[:])
    return b


def toggle(btn):
    col = btn % COLS
    row = btn // COLS
    
    if BTNS[row][col] == 0:
        BTNS[row][col] = 1
    else:
    	BTNS[row][col] = 0
    	
    if row - 1 >= 0:
        if BTNS[row-1][col] == 0:
	    BTNS[row-1][col] = 1
	else:
	    BTNS[row-1][col] = 0

    if row + 1 < ROWS:
        if BTNS[row+1][col] == 0:
            BTNS[row+1][col] = 1
        else:
            BTNS[row+1][col] = 0
    
    if col - 1 >= 0:
        if BTNS[row][col-1] == 0:
            BTNS[row][col-1] = 1
        else:
            BTNS[row][col-1] = 0

    if col + 1 < COLS:
        if BTNS[row][col+1] == 0:
            BTNS[row][col+1] = 1
        else:
            BTNS[row][col+1] = 0
	   

def lightshow():
    ctr = 0
    for i in range(ROWS):
        for j in range(COLS):
            if BTNS[i][j] == 1:
                macropad.pixels[ctr] = 0xffffff
            else:
                macropad.pixels[ctr] = 0x000000
            ctr = ctr + 1


def checkvictory():
    global score
    ctr = 0
    light_on = False
    for i in range(ROWS*COLS):
        if macropad.pixels[i] != (0, 0, 0):
            light_on = True
        ctr = ctr + 1
    if not light_on:
    	print("Victory!")
    	print("Score:", score)
    	score = 0



last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
BTNS = copyPattern(0)

while True:
    lightshow()
    position = macropad.encoder
    if position != last_position:
        # TODO: Level number display!
        score = 0
        #BTNS = []
        #BTNS.append(patterns.patterns[position % len(patterns.patterns)][:])
        BTNS = copyPattern(position % len(patterns.patterns))
        last_position = position

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch:
        # Reset level
        score = 0
        #BTNS = []
        #BTNS.append(patterns.patterns[position % len(patterns.patterns)][:])
        BTNS = copyPattern(position % len(patterns.patterns))
        
    event = macropad.keys.events.get()
    if event and event.pressed:
        score = score + 1
        toggle(event.key_number)
        lightshow()
        checkvictory()

