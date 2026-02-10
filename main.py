import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = -5
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
POWERUP_SIZE = 20
POWERUP_SPEED = 3
POWERUP_CHANCE = 0.2  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
CYAN = (50, 200, 200)
ORANGE = (255, 150, 50)
POWERUP_COLOR = (255, 215, 0)  

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick")
clock = pygame.time.Clock()

class Paddle: 
    
    def __init__(self):
        self.width = PADDLE_WIDTH 
        self.height = PADDLE_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2 
        self.y = SCREEN_HEIGHT - 40 
        self.color = BLUE
        self.speed = PADDLE_SPEED
        self.is_moving_left = False
        self.is_moving_right = False
        
    def draw(self):
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height), 
                        border_radius=5)
        pygame.draw.rect(screen, WHITE, 
                        (self.x, self.y, self.width, self.height), 
                        2, border_radius=5)
        
    def move(self):
        if self.is_moving_left and self.x > 0:
            self.x -= self.speed
        if self.is_moving_right and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed 
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    
class Balls:
    def __init__(self, x = None, y = None):
        self.x = x if x is not None else SCREEN_WIDTH // 2
        self.y = y if y is not None else SCREEN_HEIGHT // 2
        self.radius = BALL_RADIUS
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y
        self.color = WHITE

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x - self.radius // 3), int(self.y - self.radius // 3)), self.radius // 3, 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          2 * self.radius, 2 * self.radius)
    
class Game:  # Main controller class
    
    def __init__(self):
        self.paddle = Paddle() 
        self.score = 0 
        self.lives = 3
        self.level = 1 
        self.game_over = False 
        self.game_won = False

        self.font = pygame.font.SysFont(None, 36) 
        self.small_font = pygame.font.SysFont(None, 24) 
            
    def update(self):
        if self.game_over or self.game_won:  # If game ended
            return  # Don't update anything
            
        # Move paddle based on key states
        self.paddle.move()
                
    def draw(self):
        screen.fill(BLACK)
        
        # Awesome Background Grid
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
            
        self.paddle.draw() 
        
        # Draw UI text
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        

        instructions = self.small_font.render(
            "Use LEFT/RIGHT arrows to move. Catch gold stars to multiply balls!", 
            True, YELLOW)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 60))
        

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            

            game_over_text = self.font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            
            final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, YELLOW)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
            
        # Draw win screen if player won
        elif self.game_won:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            win_text = self.font.render("YOU WIN!", True, GREEN)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
            
            final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
            
            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, YELLOW)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))

def main():
    game = Game()
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    game.paddle.is_moving_left = True
                if event.key == pygame.K_RIGHT:
                    game.paddle.is_moving_right = True
                if event.key == pygame.K_r and (game.game_over or game.game_won):
                    game = Game()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.paddle.is_moving_left = False
                if event.key == pygame.K_RIGHT: 
                    game.paddle.is_moving_right = False
                    
        # Update all game objects
        game.update()
        

        game.draw()
        

        pygame.display.flip()
        

        clock.tick(60)
        
    pygame.quit() 
    sys.exit()

if __name__ == "__main__":
    main()