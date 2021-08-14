from adafruit_macropad import MacroPad
import patterns

# How big our MacroPad is:
rows = 4
cols = 3

btns = []  # We'll use this to store the patterns of on/off lights
macropad = MacroPad()  # set up the MacroPad
score = 0  # track the number of moves to solve a level
text = macropad.display_text()  # this will hold the score and level display


def copyPattern(p):
    """Copies a pattern without creating a reference to the original"""
    # This function is needed because if we just say something like:
    #    b = patterns.patterns[p]
    # then we set a reference to the original pattern, so when it's updated
    # in-game, the original is changed.  This makes resetting a level or
    # changing to a level that's already been played problematic.  So instead
    # we want to make a copy of the level in a new variable.
    b = []  # create an empty list
    for i in patterns.patterns[p]:  # find just the level we want to copy
        b.append(i[:])  # grab just that chunk of the data
    return b


def toggle(btn):
    """Toggle a button light and the lights on each side"""
    # The lights are addressed as a single 1-dimensional strand, but are
    # actually arranged in a 2-dimensional grid on the MacroPad.  So some
    # trickery is needed to find the right position!
    #
    # We want to move "down" one row each time we hit the number of columns
    # that the grid has.  So rather than real (floating point) division, we'll
    # use integer division.  We'll actually look at the whole number and the
    # remainder to find the rows/columns.
    #
    # If you want to know more about how this works, "integer division" and
    # "modulo" are the magic keywords to search for on the Internet.
    
    col = btn % cols  # modulo (%) gives the remainder after integer division
    row = btn // cols  # integer division (//) tosses out the remainder
    
    # We start with the easy bit: toggle the light for the button pressed:
    if btns[row][col] == 0:
        btns[row][col] = 1
    else:
    	btns[row][col] = 0

    # Now we need to check to see if we're at an edge.  If not, we need to
    # toggle the light on the left...
    if row - 1 >= 0:  # are we as far left as we can go?
        if btns[row-1][col] == 0:
	    btns[row-1][col] = 1
	else:
	    btns[row-1][col] = 0

    # ... and on the right...
    if row + 1 < rows:
        if btns[row+1][col] == 0:
            btns[row+1][col] = 1
        else:
            btns[row+1][col] = 0
    
    # ... and above...
    if col - 1 >= 0:
        if btns[row][col-1] == 0:
            btns[row][col-1] = 1
        else:
            btns[row][col-1] = 0

    # ... and below!
    if col + 1 < cols:
        if btns[row][col+1] == 0:
            btns[row][col+1] = 1
        else:
            btns[row][col+1] = 0
	   

def lightshow():
    """Turn the lights on or off according to what has been set in toggle()"""
    # Because the lights are a 1-d strip, we can just count through each row
    # and column in a straight line, turning lights on or off based on what
    # we set in toggle() above.
    ctr = 0  # start at the beginning, which corresponds to row 0, column 0
    for i in range(rows):  # go through each row
        for j in range(cols):  # in each row, go through each column
            if btns[i][j] == 1:  # check if we should light this one up or not
                macropad.pixels[ctr] = 0xffffff  # white
            else:
                macropad.pixels[ctr] = 0x000000  # black
            ctr = ctr + 1  # go to the next light


def checkvictory():
    """Check if all the lights have been turned off and display a score if so"""
    global score  # 'score' is a global variable, so don't create a local one here
    ctr = 0
    light_on = False  # start by assuming no lights are on
    for i in range(rows*cols):  # check all the lights from start to end...
        if macropad.pixels[i] != (0, 0, 0):  # is this light on?
            light_on = True  # we found a light on, so set this flag
        ctr = ctr + 1
    if not light_on:  # if we got all the way through with no lights on
    	text[2].text = "Victory!"  # Hooray!
    	text[3].text = "Score: " + str(score)
    	score = 0  # reset for the next level


#### Main execution starts here

# Set up the rotary encoder to track where we are
last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed

# Load the first level
btns = copyPattern(0)

# Set up the display
text[0].text = "Level 1"
text.show()

# Light up the lights
lightshow()

# Let's go!
while True:    
    # Check to see if the rotary wheel has moved:
    position = macropad.encoder
    if position != last_position:
    	# Change level
        score = 0  # it's a new level, so reset the score
        level = position % len(patterns.patterns)  # grab the next level
        # Reset any leftover score or level text on the display:
        text[0].text = "Level " + str(level + 1)
        text[2].text = ""
        text[3].text = ""
        btns = copyPattern(level)  # load the level data
        lightshow()  # update the lights
        last_position = position  # remember where the wheel is set

    # Check to see if the rotary wheel has been pressed:
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch:
        # Reset level
        score = 0
        text[2].text = ""
        text[3].text = ""
        btns = copyPattern(position % len(patterns.patterns))  # reload level data
        lightshow()  # update the lights
    
    # Look for button presses:
    event = macropad.keys.events.get()
    if event and event.pressed:  # a button was pressed
        score = score + 1  # track the score (lower is better, like golf!)
        toggle(event.key_number)  # handle the lights on/around the button
        lightshow()  # update the lights on the MacroPad
        checkvictory()  # see if they won


