 import pygame                             # importing pygame for run the code
import random                             # we are importing randomly            
import math                               # importing the math

pygame.init()

FPS = 60                                   # giving the value for "Frames per second"

WIDTH, HEIGHT = 800, 800                  # giving the values for heiht and width    
ROWS = 4
COLUMNS = 4

RECTANGLE_HEIGHT = HEIGHT // ROWS
RECTANGLE_WIDTH = WIDTH // COLUMNS
                                                           
OUTLINE_COLOR = (187, 173, 160)             # giving the outline colours to the game
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)           # giving the background colour
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20                                                # movement velocity of numbers in game

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")                             # displaying the title name that is "2048"


class Tile:
    COLORS = [                                                  # we are giving the colours of tiles
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):                      # we are defining the self,value,row,column
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECTANGLE_WIDTH
        self.y = row * RECTANGLE_HEIGHT

    def get_color(self):                                      # we are defining to get colour of function named self
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):                                            # defining to get the windows
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECTANGLE_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECTANGLE_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECTANGLE_HEIGHT)
            self.col = math.ceil(self.x / RECTANGLE_WIDTH)
        else:
            self.row = math.floor(self.y / RECTANGLE_HEIGHT)
            self.col = math.floor(self.x / RECTANGLE_WIDTH)

    def move(self, delta):                                          # defining to move the numbers from one place to another
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):                                              # we are drawing the lines o rfows
    for row in range(1, ROWS):
        y = row * RECTANGLE_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for i in range(1, COLUMNS):                                          # we are drawing the lines of columns
        x = i * RECTANGLE_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):                                             # we are defining to draw  the tiles
    window.fill(BACKGROUND_COLOR)

    for i in tiles.values():
        i.draw(window)

    draw_grid(window)

    pygame.display.update()                           # we are updating the process 


def get_random_pos(tiles):                            # defining to get random position  of tiles
    row = None
    column = None
    while True:
        row = random.randrange(0, ROWS)
        column = random.randrange(0, COLUMNS)

        if f"{row}{column}" not in tiles:
            break

    return row, column


def move_tiles(window, tiles, clock, direction):                # defining to move the tiles
    updated = True
    blocks = set()

    if direction == "left":                                    # we are moving the tiles to left
        sort_func = lambda x : x.col
        reverse = False
        delta = (-MOVE_VEL, 0)                                  # now this tiles are moving left so, it has negative velocity
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECTANGLE_WIDTH + MOVE_VEL
        )
        function = True
    elif direction == "right":                                          # we are moving the tiles to right
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)                                           # now this tiles are moving right so, it has positive velocity
        boundary_check = lambda tile: tile.col == COLUMNS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECTANGLE_WIDTH + MOVE_VEL < next_tile.x
        )
        function = False
    elif direction == "up":                                                   # we are moving the tiles to up
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)                                                # now this tiles are moving up so, it has negative velocity
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECTANGLE_HEIGHT + MOVE_VEL
        )
        function = True
    elif direction == "down":                                                  # we are moving the tiles to down
        sort_func= lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)                                                  #  now this tiles are down up so, it has positive velocity
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECTANGLE_HEIGHT + MOVE_VEL < next_tile.y
        )
        function = False

    while updated:
        clock.tick(FPS)                                  # we are inserting the FPS in time
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):ng
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):               # we are merging the numbers
                    tile.move(delta)
                else:
                    next_tile.value *= 2                    # if two same numbers are merge they will double
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set(function)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)

              
def end_move(tiles):                      # defining the end move of tiles
    if len(tiles) == 16:                 # if no more space to move then it shows lost
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles():                                 # we are generating the new tiles
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)              # we will get that numbers in random positions
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for game in pygame.event.get():
            if game.type == pygame.QUIT:
                run = False
                break

            if game.type == pygame.KEYDOWN:
                if game.key == pygame.K_LEFT:                   # if we press the left key  they will go left
                    move_tiles(window, tiles, clock, "left")
                if game.key == pygame.K_RIGHT:                   #if we press the right key they will go right
                    move_tiles(window, tiles, clock, "right")
                if game.key == pygame.K_UP:                      # if we press the up key they will go up
                    move_tiles(window, tiles, clock, "up")
                if game.key == pygame.K_DOWN:                    #if we press the down key they will go down
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":                                # we are testing the code                                 
    main(WINDOW)
