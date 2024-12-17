def init():
    # Common to all games
    global dt
    global objs
    global texts
    global window

    dt = 0
    objs = []
    texts = []
    window = None

    # Game specific
    global selected
    global deck

    selected = None
    deck = None
