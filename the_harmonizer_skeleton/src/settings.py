###########################
# DO NOT CHANGE ANYTHING. #
###########################

# ---COLORS--- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
NUMBERCOLOR = (255, 0, 0)
BGCOLOUR = DARKGRAY

# ---GAME SETTINGS--- #
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "The Harmonizer"
BOARDSIZE = 400
GAMESIZE = [5, 5]
TILESIZE = BOARDSIZE // max(GAMESIZE[0], GAMESIZE[1])

# ---LEVELS--- #
# 0: Empty
# 1: Red
# 2: Blue
# 3: Purple
# 4: Wall
LEVELS = [["04442",
           "04000",
           "00040",
           "04040",
           "10040"],
          ["0400402",
           "0000040",
           "4004000",
           "0004004",
           "0000400",
           "0400000",
           "1004404"],
          ["404440040",
           "004000040",
           "040400400",
           "040140004",
           "000420044",
           "404004000",
           "400004000",
           "044040040",
           "000044400"]]

# ---STARTING POSITION--- #
START = [(WIDTH - BOARDSIZE) // 2, (HEIGHT - BOARDSIZE) // 4]
