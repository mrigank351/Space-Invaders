import pygame, sys, random
from agent import Agent
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = pygame.font.Font("Font/monogram.ttf", 40)
level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)
q_agent = Agent(game, num_states=10, num_actions=2)  #mml

# Define the number of episodes for training
num_episodes = 10000                                    #mml

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

# Initialize the state
state = game.get_state()

for episode in range(num_episodes):
    # Reset the game at the start of each episode
    game.reset()
    
    while game.run:
        # Choose an action
        action = q_agent.choose_action(state)
        
        # Perform the action and get the reward
        reward = game.step(action)
        
        # Get the next state
        next_state = game.get_state()
        
        # Update the Q-values
        q_agent.update_q_table(state, action, reward, next_state)
        
        # Move to the next state
        state = next_state

        #Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SHOOT_LASER and game.run:
                game.alien_shoot_laser()

            if event.type == MYSTERYSHIP and game.run:
                game.create_mystery_ship()
                pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and game.run == False:
                game.reset()

        #Updating
        if game.run:
            game.spaceship_group.update()
            game.move_aliens()
            game.alien_lasers_group.update()
            game.mystery_ship_group.update()
            game.check_for_collisions()

        #Drawing
        screen.fill(GREY)

        #UI
        pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

        if game.run:
            screen.blit(level_surface, (570, 740, 50, 50))
        else:
            screen.blit(game_over_surface, (570, 740, 50, 50))

        x = 50
        for life in range(game.lives):
            screen.blit(game.spaceship_group.sprite.image, (x, 745))
            x += 50

        screen.blit(score_text_surface, (50, 15, 50, 50))
        formatted_score = str(game.score).zfill(5)
        score_surface = font.render(formatted_score, False, YELLOW)
        screen.blit(score_surface, (50, 40, 50, 50))
        screen.blit(highscore_text_surface, (550, 15, 50, 50))
        formatted_highscore = str(game.highscore).zfill(5)
        highscore_surface = font.render(formatted_highscore, False, YELLOW)
        screen.blit(highscore_surface, (625, 40, 50, 50))

        game.spaceship_group.draw(screen)
        game.spaceship_group.sprite.lasers_group.draw(screen)
        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)
        game.aliens_group.draw(screen)
        game.alien_lasers_group.draw(screen)
        game.mystery_ship_group.draw(screen)

        pygame.display.update()
        clock.tick(60)