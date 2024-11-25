import pygame
import random

# initialize pygame
pygame.init()

# screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space war game")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# fonts
font = pygame.font.SysFont(None, 36)

# game variables
player_x, player_y = WIDTH // 2, HEIGHT - 70  # initial position of the shooter
player_speed = 5  # speed of the player
bullet_speed = -7  # speed of bullets
enemy_speed = 3  # speed of enemies
well_wisher_speed = 2  # speed of well-wishers

bullets = []  # list to store active bullets
enemies = []  # list to store active enemies
well_wishers = []  # list to store active well-wishers

score = 0  # player's score
lives = 3  # number of lives
game_over = False  # game state

# function to draw text on the screen
def draw_text(text, x, y, color):
    screen.blit(font.render(text, True, color), (x, y))

# function to spawn an enemy at a random x-position
def spawn_enemy():
    x = random.randint(0, WIDTH - 30)
    enemies.append([x, 0])

# function to spawn a well-wisher at a random x-position
def spawn_well_wisher():
    x = random.randint(0, WIDTH - 30)
    well_wishers.append([x, 0])

# game loop
clock = pygame.time.Clock()
while not game_over:
    screen.fill(BLACK)  # clear the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:  # move left
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:  # move right
        player_x += player_speed
    if keys[pygame.K_SPACE]:  # shoot bullets
        if len(bullets) < 5:  # limit the number of bullets
            bullets.append([player_x + 25, player_y])  # center the bullet to the shooter

    # update bullets
    bullets = [[x, y + bullet_speed] for x, y in bullets if y > 0]

    # spawn enemies and well-wishers randomly
    if random.randint(1, 100) <= 2:  # small chance to spawn an enemy
        spawn_enemy()
    if random.randint(1, 100) <= 1:  # smaller chance to spawn a well-wisher
        spawn_well_wisher()

    # update enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed  # move enemy down
        if enemy[1] > HEIGHT:  # remove enemy if it goes out of screen
            enemies.remove(enemy)

    # update well-wishers
    for well_wisher in well_wishers[:]:
        well_wisher[1] += well_wisher_speed  # move well-wisher down
        if well_wisher[1] > HEIGHT:  # remove well-wisher if it goes out of screen
            well_wishers.remove(well_wisher)

    # check collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if abs(bullet[0] - enemy[0]) < 30 and abs(bullet[1] - enemy[1]) < 30:
                bullets.remove(bullet)  # remove bullet
                enemies.remove(enemy)  # remove enemy
                score += 1  # increment score
                break
        for well_wisher in well_wishers[:]:
            if abs(bullet[0] - well_wisher[0]) < 30 and abs(bullet[1] - well_wisher[1]) < 30:
                bullets.remove(bullet)  # remove bullet
                well_wishers.remove(well_wisher)  # remove well-wisher
                lives -= 1  # decrement lives
                break

    # draw player as a rectangle
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))  # shooter is a blue rectangle

    # draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, bullet, 5)

    # draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, RED, enemy, 15)

    # draw well-wishers
    for well_wisher in well_wishers:
        pygame.draw.circle(screen, GREEN, well_wisher, 15)

    # display score and lives
    draw_text(f"score: {score}", 10, 10, WHITE)
    draw_text(f"lives: {lives}", 10, 50, WHITE)

    # check for game over
    if lives <= 0:
        game_over = True

    pygame.display.flip()  # update the display
    clock.tick(60)  # set the frame rate

# end screen
screen.fill(BLACK)  # clear the screen
draw_text("game over", WIDTH // 2 - 100, HEIGHT // 2 - 20, RED)
draw_text(f"final score: {score}", WIDTH // 2 - 100, HEIGHT // 2 + 20, WHITE)
pygame.display.flip()
pygame.time.wait(3000)  # wait for a few seconds before closing

pygame.quit()
