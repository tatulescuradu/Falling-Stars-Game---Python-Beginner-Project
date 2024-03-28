import pygame
import time
import random
pygame.font.init()

"""A game simulating Chicken Invaders.

    This game involves avoiding falling stars and keeping the player alive for as long as possible.
"""

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Falling Stars')

BG = pygame.transform.scale(pygame.image.load("CI5Galaxy.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PLAYER_VEL = 8

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("arial", 30)

def draw(player, elapsed_time, stars):
    """Draws the game elements on the screen.

    Args:
        player (pygame.Rect): Rect representing the player.
        elapsed_time (float): Time elapsed since the beginning of the game.
        stars (list): List of pygame.Rect objects representing the stars.
    """
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "yellow", player)

    for star in stars:
        pygame.draw.rect(WIN, 'white', star)

    pygame.display.update()


def main():
    """The main function of the game."""
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    """Initializing parameters for star appearance and movement"""
    star_add_increment = 2000  # Initial interval between new star appearances
    star_count = 0  # Counter to determine when new stars should be added
    stars = []  # List containing Rect objects for the stars
    hit = False  # Variable to indicate if the player has been hit by a star

    while run:
        """Updating the time elapsed since the beginning of the game"""
        star_count += clock.tick(40)
        elapsed_time = time.time() - start_time

        """Adding new stars to the game based on the set interval"""
        if star_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)  # Stars appear above x
                stars.append(star)

            """ Reducing the time interval between new star appearances to increase game difficulty"""
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            """Checking the events in the game."""
            if event.type == pygame.QUIT:
                """Closes the game if the user presses the window close button."""
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            """Move the player to the left if the corresponding key is pressed and 
            does not exceed the left edge of the screen."""
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            """Move the player to the right if the corresponding key is pressed and 
            does not exceed the right edge of the screen."""
            player.x += PLAYER_VEL

        for star in stars[:]:
            """Update the position of the stars and detect collisions with the player."""
            star.y += STAR_VEL
            if star.y > HEIGHT:
                """Remove stars that have exceeded the bottom edge of the screen."""
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                """Remove stars that have collided with the player."""
                stars.remove(star)
                hit = True
                break

        if hit:
            """If the player has been hit by a star, display a message 
            and pause the game for a few seconds."""
            lost_text = FONT.render("You lost!", 1, 'white')
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    """The main() function ensures that the game runs until the user decides to close it or until the game's end conditions are met, such as the player being hit by a star."""
    main()
