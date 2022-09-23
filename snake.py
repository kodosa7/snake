# *******************************
# SNAKE game from PyLadies course
#      by ELS (c) 2020-2022
# *******************************

import pyglet, random, os, hashlib, json
from pathlib import Path
from pyglet.window import key


def first_run_initial_settings():
    global IS_TITLE
    global HISCORE
    global HISCORE_FILENAME

    IS_TITLE = True
    HISCORE = [0]
    HISCORE_FILENAME = 'snake_hiscore'


def initial_settings():
    """ set global variables """

    global TILES_DIRECTORY
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global TILE_SIZE
    global TILE_COUNT_X
    global TILE_COUNT_Y
    global SNAKE
    global FOOD
    global FOOD_TYPE
    global STEPS
    global PRESSED_KEYS
    global SCORE
    global DIRECTION
    global SPEED
    global IS_END

    TILES_DIRECTORY = Path('assets/gfx')
    WINDOW_WIDTH = 960   # not recommended to change window size
    WINDOW_HEIGHT = 768  # due to fixed size of background picture
    TILE_SIZE = WINDOW_WIDTH // 20
    TILE_COUNT_X = (WINDOW_WIDTH // TILE_SIZE) - 1
    TILE_COUNT_Y = (WINDOW_HEIGHT // TILE_SIZE) - 1
    SNAKE = [(2, 2), (3, 2), (4, 2)]
    FOOD = [(2, 5)]
    FOOD_TYPE = "1"
    STEPS = [0]
    PRESSED_KEYS = set()
    SCORE = [0]
    DIRECTION = (1, 0)  # default direction is to the right
    SPEED = .2
    IS_END = False


def encrypt_and_write_hiscore(item):
    """ encrypts HISCORE value (item) and writes value and hash into json file """

    content = {}
    content[item] = hashlib.md5(bytes(item, 'ascii')).hexdigest()

    with open(HISCORE_FILENAME, 'w') as hsf:
        json.dump(content, hsf)
        hsf.close()


def create_hiscore_file():
    """ create hiscore json file if not exist and write HISCORE value
        (which is "0" if file doesn't exist yet) and generated hash into it """

    # write
    item = "0"
    if not os.path.exists(HISCORE_FILENAME):
        encrypt_and_write_hiscore(item)


def collect_filenames():
    """ this makes a dict with picture names from the directory """

    all_png_files = list(TILES_DIRECTORY.glob('*.png'))
    pictures = {}
    for path in all_png_files:
        pictures[path.stem] = pyglet.image.load(path)

    return pictures


def title_screen():
    """ title screen """

    global IS_TITLE
    IS_TITLE = True

    window.clear()
    pyglet.clock.unschedule(tik)

    title_name_picture.x = (window.width - title_name_picture.width) // 2
    title_name_picture.y = window.height // 1.3
    title_name_picture.draw()

    label_credits_text = pyglet.text.Label('- by ELS -',
                            font_name='16bfZX',
                            font_size=36,
                            color=(210, 0, 120, 230),
                            x=window.width // 2, y=(window.height // 1.35),
                            anchor_x='center', anchor_y='center')
    label_credits_text.draw()

    snake_picture.x = (window.width - snake_picture.width) // 2
    snake_picture.y = window.height // 2.7
    snake_picture.draw()

    pyladies_picture.x = (window.width - pyladies_picture.width) // 2
    pyladies_picture.y = window.height // 4.6
    pyladies_picture.draw()

    label_press_enter_text = pyglet.text.Label('+ + + Press [ENTER] to start + + +',
                            font_name='16bfZX',
                            font_size=36,
                            color=(230, 230, 0, 200),
                            x=window.width // 2, y=(window.height // 6.2),
                            anchor_x='center', anchor_y='center')
    label_press_enter_text.draw()


def game_over(message):
    """ game over screen """

    global IS_END
    IS_END = True

    # if new HISCORE is reached, delete old file and write it to the new one
    if SCORE[0] > HISCORE[0]:
        HISCORE[0] = SCORE[0]

        hiscore_file_name = "snake_hiscore"
        if os.path.exists(hiscore_file_name):
            os.remove(hiscore_file_name)
        else:
            print("The snake_hiscore file does not exist")
        
        # write
        item = str(HISCORE[0])
        encrypt_and_write_hiscore(item)

    window.clear()
    pyglet.clock.unschedule(tik)
    label_game_over_score = pyglet.text.Label('Score: '+str(SCORE[0]),
                            font_name='16bfZX',
                            font_size=48,
                            color=(230, 230, 230, 230),
                            x=window.width // 2, y=(window.height // 2) - 48,
                            anchor_x='center', anchor_y='center')
    label_game_over_score.draw()

    label_game_over_hiscore = pyglet.text.Label('High score: '+str(HISCORE[0]).zfill(4),
                            font_name='16bfZX',
                            font_size=48,
                            color=(230, 230, 230, 230),
                            x=window.width // 2, y=(window.height // 2) - 96,
                            anchor_x='center', anchor_y='center')
    label_game_over_hiscore.draw()

    label_bye = pyglet.text.Label(message,
                            font_name='16bfZX',
                            font_size=36,
                            bold=True,
                            color=(220, 220, 220, 220),
                            x=window.width // 2, y=(window.height // 2) + 128,
                            anchor_x='center', anchor_y='center')
    label_bye.draw()

    label_escape = pyglet.text.Label('Press [ENTER] to play again or [ESC] to exit',
                            font_name='16bfZX',
                            font_size=36,
                            color=(230, 230, 0, 200),
                            x=window.width // 2, y=(window.height // 4),
                            anchor_x='center', anchor_y='center')
    label_escape.draw()

    game_over_picture.x = (window.width - game_over_picture.width) // 2
    game_over_picture.y = window.height // 2
    game_over_picture.draw()


def tik(t):
    """ sets time interval """

    STEPS[0] += 1

    # add new snake tile and delete last tile
    current_x = SNAKE[-1][0]
    current_y = SNAKE[-1][1]
    new_x = current_x + DIRECTION[0]
    new_y = current_y + DIRECTION[1]
    SNAKE.append((new_x, new_y))
    del SNAKE[0]

    if DIRECTION == (1, 0):
        snake.x = snake.x + 64
    if DIRECTION == (-1, 0):
        snake.x = snake.x - 64
    if DIRECTION == (0, 1):
        snake.y = snake.y + 64
    if DIRECTION == (0, -1):
        snake.y = snake.y - 64


def key_press(symbol, modificators):
    """ tests pressed keys (WSAD or arrows) """

    if symbol == key.W or symbol == key.UP:
        PRESSED_KEYS.add((0, 1))
    if symbol == key.S or symbol == key.DOWN:
        PRESSED_KEYS.add((0, -1))
    if symbol == key.A or symbol == key.LEFT:
        PRESSED_KEYS.add((-1, 0))
    if symbol == key.D or symbol == key.RIGHT:
        PRESSED_KEYS.add((1, 0))
    if symbol == key.RETURN and IS_END:
        restart_game()
    if symbol == key.RETURN and IS_TITLE:
        restart_game()


def key_release(symbol, modificators):
    """ tests released keys """

    if symbol == key.W or symbol == key.UP:
        PRESSED_KEYS.discard((0, 1))
    if symbol == key.S or symbol == key.DOWN:
        PRESSED_KEYS.discard((0, -1))
    if symbol == key.A or symbol == key.LEFT:
        PRESSED_KEYS.discard((-1, 0))
    if symbol == key.D or symbol == key.RIGHT:
        PRESSED_KEYS.discard((1, 0))


def playfield_collision_test():
    """ border collision test """

    reason_message = "The snake ran out of the playground"
    if SNAKE[-1][0] > TILE_COUNT_X or SNAKE[-1][0] < 0:
        game_over(reason_message)
        return True

    if SNAKE[-1][1] > TILE_COUNT_Y or SNAKE[-1][1] < 0:
        game_over(reason_message)
        return True

    return False


def eat_itself():
    """ if snake eats itself """

    if SNAKE[-1] in SNAKE[:-2]:
        game_over("The snake ate itself")
        return True

    return False


def test_keys():
    """ assign pressed key to a direction """

    global DIRECTION
    if (1, 0) in PRESSED_KEYS:
        DIRECTION = (1, 0)
    if (-1, 0) in PRESSED_KEYS:
        DIRECTION = (-1, 0)
    if (0, 1) in PRESSED_KEYS:
        DIRECTION = (0, 1)
    if (0, -1) in PRESSED_KEYS:
        DIRECTION = (0, -1)


def eat_food():
    """ eat food function """

    global FOOD_TYPE

    new_food_x = random.randint(0, TILE_COUNT_X)
    new_food_y = random.randint(0, TILE_COUNT_Y)

    if SNAKE[-1] == FOOD[-1]:  # eat with snake's head

        # while the generated food is on snake's position,
        # keep generating new one somewhere else
        # until it's generated outside the snake
        while ((new_food_x, new_food_y)) in SNAKE[:-1]:
            new_food_x = random.randint(0, TILE_COUNT_X)
            new_food_y = random.randint(0, TILE_COUNT_Y)

        last_food = FOOD_TYPE
        FOOD_TYPE = str(random.randint(1, 5))  # random type of food

        FOOD.append((new_food_x, new_food_y))
        del FOOD[0]

        # add piece of snake to the end
        SNAKE.insert(0, (SNAKE[0][0], SNAKE[0][1]))

        if last_food == "5":  # if food is pokeball, increase score by 5 points
            SCORE[0] += 5
        else:  # else increase score by 1 point
            SCORE[0] += 1



def get_image_name(index):
    """ gets tile name from filename """

    x_actual, y_actual = SNAKE[index]
    name_prev = 'tail'
    name_next = 'head'

    # test of current tile and previous tile
    if index == 0:  # if index is 0, it's always 'tail'
        name_prev = "tail"
    else:
        x_prev, y_prev = SNAKE[index - 1]  # else it sucks

        if x_actual == x_prev and y_actual == y_prev - 1:
            name_prev = "top"
        if x_actual == x_prev and y_actual == y_prev + 1:
            name_prev = "bottom"
        if x_actual == x_prev - 1 and y_actual == y_prev:
            name_prev = "right"
        if x_actual == x_prev + 1 and y_actual == y_prev:
            name_prev = "left"

    # test of current tile and next tile
    if index == len(SNAKE) - 1:  # if index is last, it's 'head'
        name_next = "head"
    else:
        x_actual, y_actual = SNAKE[index]  # else it sucks
        x_next, y_next = SNAKE[index + 1]

        if x_actual == x_next and y_actual == y_next - 1:
            name_next = "top"
        if x_actual == x_next and y_actual == y_next + 1:
            name_next = "bottom"
        if x_actual == x_next - 1 and y_actual == y_next:
            name_next = "right"
        if x_actual == x_next + 1 and y_actual == y_next:
            name_next = "left"

    return name_prev + "-" + name_next


def draw_score():
    """ draws score text """

    # font_size parameter reflects window size
    label_score = pyglet.text.Label("SC "+str(SCORE[0]).zfill(4),
                            font_name='16bfZX',
                            font_size=int(TILE_SIZE) * 1.5,
                            color=(255, 255, 255, 240),
                            x=((window.width / 2) / 2) - int(TILE_SIZE // 2) + 75, y=window.height - (TILE_SIZE * 1.1),
                            anchor_x='center')  # + 75 is manual justify to match the hi_score display position

    label_score.draw()

    label_hi_score = pyglet.text.Label("HI "+str(HISCORE[0]).zfill(4),
                            font_name='16bfZX',
                            font_size=int(TILE_SIZE) * 1.5,
                            color=(255, 255, 255, 240),
                            x=(((window.width / 2) / 2) * 3) - int(TILE_SIZE // 2), y=window.height - (TILE_SIZE * 1.1),
                            anchor_x='center')

    label_hi_score.draw()

    label_steps = pyglet.text.Label(str(STEPS[0]).zfill(5),
                            font_name='16bfZX',
                            font_size=int(TILE_SIZE // 2),
                            color=(48, 114, 255, 255),
                            x=TILE_SIZE // 6, y=window.height - (TILE_SIZE // 2))
    label_steps.draw()


def draw_all():
    """ main draw function """

    window.clear()

    if IS_TITLE:
        title_screen()

    else:
        playfield_picture.x = 0
        playfield_picture.y = 0
        playfield_picture.draw()

        draw_score()

        # sprite's edges smoothing
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    
        test_keys()
        eat_food()

        if playfield_collision_test() == False and eat_itself() == False:

            # draw snake
            # not mine :'(
            for index, value in enumerate(SNAKE):
                snake_piece_img_name = get_image_name(index)
                snake_cell = picture_names[snake_piece_img_name]
                snake_cell.blit(value[0] * TILE_SIZE, value[1] * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

            # draw food
            # copies snake drawing idea above, but uses "apple" image only
            for index, value in enumerate(FOOD):
                food_cell = picture_names["food" + FOOD_TYPE]
                food_cell.blit(value[0] * TILE_SIZE, value[1] * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)


def read_hiscore_from_file():
    with open(HISCORE_FILENAME, 'r') as hsf:
        content = json.load(hsf)
        key = list(content.keys())[0]
        value = list(content.values())[0]
        
        if hashlib.md5(bytes(key, 'ascii')).hexdigest() == value:
            HISCORE[0] = int(key)
        else:
            print("The hiscore hash doesn't match, it may have been changed!")
            hsf.close()
            quit()

        hsf.close()


def restart_game():
    """ sets all global variables again (except HISCORE and IS_TITLE) for game restart """

    initial_settings()

    global IS_TITLE
    IS_TITLE = False

    read_hiscore_from_file()

    window.clear()
    pyglet.clock.schedule_interval(tik, SPEED)


# first start

# set vars before initial settings to show title screen and reset hiscore
first_run_initial_settings()

create_hiscore_file()  # create hiscore file
read_hiscore_from_file()  # read hiscore from file

# set initial variables
initial_settings()

window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # set window size

picture_names = collect_filenames()  # get dict with tile names

# set sprites
snake = pyglet.sprite.Sprite(picture_names['left-dead'])

for food_number in range(1, 5):
    food = pyglet.sprite.Sprite(picture_names['food' + str(food_number)])

game_over_picture = pyglet.sprite.Sprite(picture_names['game_over'])
title_name_picture = pyglet.sprite.Sprite(picture_names['title'])
snake_picture = pyglet.sprite.Sprite(picture_names['snake'])
pyladies_picture = pyglet.sprite.Sprite(picture_names['pyladies'])
playfield_picture = pyglet.sprite.Sprite(picture_names['playfield'])

# load font
pyglet.font.add_file('assets/font/16bfZX.ttf')

# main loop
if __name__ == "__main__":
    window.push_handlers(
    on_draw=draw_all,
    on_key_press=key_press,
    on_key_release=key_release,
    )

    pyglet.clock.schedule_interval(tik, SPEED)

    pyglet.app.run()
