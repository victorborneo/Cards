def init():
    # Common to all games
    global dt
    global objs
    global texts
    global window
    global settings

    dt = 0
    objs = []
    texts = []
    window = None
    settings = None

    # Game specific
    global selected
    global deck

    selected = None
    deck = None
