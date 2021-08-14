from adafruit_macropad import MacroPad
import patterns

ROWS = 4
COLS = 3

BTNS = []
macropad = MacroPad()
score = 0
text = macropad.display_text()


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
    	text[2].text = "Victory!"
    	text[3].text = "Score: " + str(score)
    	score = 0



last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
BTNS = copyPattern(0)
text[0].text = "Level 1"
text.show()

while True:
    lightshow()
    position = macropad.encoder
    if position != last_position:
    	# Change level
        score = 0
        level = position % len(patterns.patterns)
        text[0].text = "Level " + str(level + 1)
        text[2].text = ""
        text[3].text = ""
        BTNS = copyPattern(level)
        last_position = position

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch:
        # Reset level
        score = 0
        text[2].text = ""
        text[3].text = ""
        BTNS = copyPattern(position % len(patterns.patterns))
        
    event = macropad.keys.events.get()
    if event and event.pressed:
        score = score + 1
        toggle(event.key_number)
        lightshow()
        checkvictory()


