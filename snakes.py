import pygame
import random

from objects.snake import Snake
from objects.food import Food

GAME_WIDTH = 640
GAME_HEIGHT = 480
BACKGROUND_COLOR = (0xFF, 0xA5, 0x00)
FRAMERATE = 32
ARROW_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

def initialize_screen():
    # Initialize the screen and game objects.
    pygame.init()
    pygame.display.set_caption('SNAKES - Press <Esc> to Quit, <Space> to Restart')
    ####
    # TODO:
    # Set the key repeat speed (so that holding down an arrow key will
    # continue to move the snake).
    ####

    return pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))


def move_bad_snake(bad_snake, game_surface, current_direction):
    bad_snake.move(current_direction, game_surface)

    if random.random() > .75:
        current_direction = random.choice(ARROW_KEYS)

    return current_direction


def detect_collisions(good_snake, bad_snake):
    """
    Detect collisions between the Good Snake and the Bad Snake, and
    between the Good Snake and itself.

    Returns True if there's been a collision and False otherwise.
    """
    for python_area in good_snake.get_rects():
        for bad_snake_area in bad_snake.get_rects():
            if python_area.colliderect(bad_snake_area):
                return True

    # detect collisions with ourself
    if good_snake.head_hit_body():
        return True

    return False


def create_food(food, game_surface):
    while len(food) < 5:
        food.append(Food(game_surface))

    return food


def play_game():
    game_surface = initialize_screen()

    # Create our snake.
    good_snake = Snake(pygame.Color('purple'),
                       [random.randint(0, GAME_WIDTH),
                        random.randint(0, GAME_HEIGHT)])
    good_snake.update(game_surface)

    # Create the bad snake.
    bad_snake = Snake(pygame.Color('grey'),
                      [random.randint(0, GAME_WIDTH),
                       random.randint(0, GAME_HEIGHT)])
    bad_snake.update(game_surface)
    bad_snake_direction = random.choice(ARROW_KEYS)

    snake_food = create_food([], game_surface)

    game_clock = pygame.time.Clock()
    while True:
        game_clock.tick(FRAMERATE)
        game_surface.fill(BACKGROUND_COLOR)

        # Detect and respond to user keypresses.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                elif e.key in ARROW_KEYS:
                    good_snake.move(e.key, game_surface)

        # Move the bad snake.
        bad_snake_direction = move_bad_snake(bad_snake, game_surface,
                                             bad_snake_direction)

        # Detect any collisions.
        if detect_collisions(good_snake, bad_snake):
            return restart(game_surface)

        # Have both snakes eat any available food.
        good_snake.try_to_eat(snake_food)
        bad_snake.try_to_eat(snake_food)

        # Refresh the food supply.
        snake_food = create_food(snake_food, game_surface)

        # Update the snake and food pixels.
        good_snake.update(game_surface)
        bad_snake.update(game_surface)
        for f in snake_food:
            f.update(game_surface)

        pygame.display.update()


def restart(game_surface):
    """
    Display a GAME OVER screen and return True if a new game should be
    started or False if the user wants to quit.
    """
    # Clear the background.
    game_surface.fill(BACKGROUND_COLOR)

    # Draw the game over message.
    text = 'GAME OVER'
    font = pygame.font.SysFont('Tahoma', 128)
    line = font.render(text, True, (20, 20, 220))

    x_center = (GAME_WIDTH / 2) - (line.get_width() / 2)
    y_center = (GAME_HEIGHT / 2) - (line.get_height() / 2)

    game_surface.blit(line, line.get_rect().move((x_center, y_center)))
    pygame.display.update()

    # Wait for the user to either restart or quit.
    while True:
        ####
        # TODO:
        # Handle the 3 key presses we care about for determining
        # whether to restart or quite the game:
        # 1. QUIT (quit, caused by closing the game window)
        # 2. ESCAPE (quit)
        # 3. SPACE (restart)
        ####
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # The user closed the window.
                return False


if __name__ == '__main__':
    still_playing = True
    while still_playing:
        still_playing = play_game()
