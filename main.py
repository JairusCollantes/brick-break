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
BALL_SPEED_Y = 5
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
        self.speed_x = BALL_SPEED_X * random.randint(-100,100) / 100
        self.speed_y = BALL_SPEED_Y
        self.color = WHITE
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, YELLOW, (int(self.x - self.radius // 3), int(self.y - self.radius // 3)), self.radius // 3, 2)

    def move(self):
        if not self.active:
            return
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:  
            self.speed_x *= -1
        if self.y <= self.radius:   
            self.speed_y *= -1
        
        if self.y >= SCREEN_HEIGHT + self.radius:  
            self.active = False

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          2 * self.radius, 2 * self.radius)

class Bricks:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.active = True
        self.hit_count = 0
        self.max_hits = 1
        
        if color == RED:
            self.max_hits = 2

    def draw(self):
        if not self.active:
            return
    
        pygame.draw.rect(screen, self.color, 
                            (self.x, self.y, self.width, self.height), 
                            border_radius=3)
        pygame.draw.rect(screen, tuple(min(c + 40, 255) for c in self.color), 
                            (self.x, self.y, self.width, self.height), 2, border_radius=3)
        
        if self.hit_count > 0:
            crack_color = (50,50,5)
            pygame.draw.line(screen, crack_color, 
                            (self.x + self.width // 4, self.y + self.height // 4), 
                            (self.x + 3 * self.width // 4, self.y + 3 * self.height // 4), 2)
            pygame.draw.line(screen, crack_color, 
                            (self.x + 3 * self.width // 4, self.y + self.height // 4), 
                            (self.x + self.width // 4, self.y + 3 * self.height // 4), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self):
        self.hit_count += 1
        if self.hit_count >= self.max_hits:
            self.active = False

class PowerUp:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = POWERUP_SPEED 
        self.color = POWERUP_COLOR 
        self.type = "multiball" # Why type? Only one type for now, but could expand later
        self.active = True
        
    def draw(self):
        if not self.active:
            return
        
        # Star for multiball power-up like wtf why is it so hard to draw a star in pygame
        points = [] 
        for i in range(5):
            angle = 2 * 3.14159 * i / 5 - 3.14159 / 2

            outer_x = self.x + self.size * 0.9 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
            outer_y = self.y + self.size * 0.9 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
            points.append((outer_x, outer_y))
            
            inner_angle = angle + 3.14159 / 5

            inner_x = self.x + self.size * 0.4 * pygame.math.Vector2(1, 0).rotate(inner_angle * 57.3).x
            inner_y = self.y + self.size * 0.4 * pygame.math.Vector2(1, 0).rotate(inner_angle * 57.3).y
            points.append((inner_x, inner_y))
            
        pygame.draw.polygon(screen, self.color, points)
        
        font = pygame.font.SysFont(None, 18) 
        text = font.render("3x", True, BLACK)
        screen.blit(text, (self.x - 8, self.y - 5))
        
    def move(self):
        self.y += self.speed
        
        if self.y > SCREEN_HEIGHT:
            self.active = False 
            
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2,
                          self.y - self.size//2,
                          self.size,
                          self.size)

class Game:  # Main controller class
    
    def __init__(self):
        self.paddle = Paddle() 
        self.score = 0 
        self.lives = 3
        self.level = 0
        self.game_over = False 
        self.game_won = False
        self.balls = [Balls()]
        self.bricks = []
        self.powerups = []
        self.cheat_mode = False
        
        self.font = pygame.font.SysFont(None, 36) 
        self.small_font = pygame.font.SysFont(None, 24) 
    
    def create_bricks(self):
    
        self.bricks = []
       
        rows = min(5 + (self.level - 1), 8)
        cols = BRICK_COLS
        
        total_width = cols * BRICK_WIDTH + (cols - 1) * BRICK_PADDING
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        red_chance = 0.1 + (self.level - 10) * 0.2
        base_colors = [PURPLE, GREEN, BLUE, YELLOW]
        
        for row in range(rows):
            for col in range(cols):
                # Calculate brick position
                brick_x = start_x + col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP

                if random.random() < red_chance:
                    color = RED
                else:
                    color = random.choice(base_colors)
                    
                if random.random() < 0.25:
                    continue
                else:
                    self.bricks.append(Bricks(brick_x, brick_y, color))
    
    def collision_detection(self):
        for ball in self.balls:
            if not ball.active:
                continue
            
            if ball.get_rect().colliderect(self.paddle.get_rect()):
                relative_intersect_x = (self.paddle.x + (self.paddle.width // 2) - ball.x) / self.paddle.width
                bounce = relative_intersect_x * 0.8
                ball.speed_x = -BALL_SPEED_X * relative_intersect_x * 1.5
                ball.speed_y = (ball.speed_y * -1) -0.2
                if self.cheat_mode:
                    self.balls.append(Balls())
                else:
                    ball.y = self.paddle.y - ball.radius - 1         
            for brick in self.bricks:
                if brick.active and ball.get_rect().colliderect(brick.get_rect()):
                    brick_rect = brick.get_rect()
                    ball_rect = ball.get_rect()
                    
                    # Calculate overlap amounts prevents ball from getting stuck in bricks
                    dx = (ball_rect.centerx - brick_rect.centerx) / (brick_rect.width / 2)
                    dy = (ball_rect.centery - brick_rect.centery) / (brick_rect.height / 2)
                    
                    # Bounce based on which side was hit
                    if abs(dx) > abs(dy): 
                        ball.speed_x *= -1 
                    else:
                        ball.speed_y *= -1
                    
                    brick.hit() 
                    self.score += 10
                    if self.cheat_mode:
                        self.balls.append(Balls())
                    
                    if brick.active == False and random.random() < POWERUP_CHANCE:
                        self.powerups.append(PowerUp(brick.x + brick.width // 2, brick.y + brick.height // 2))
                    
                    break  # Only handle one brick collision per frame
                
            for powerup in self.powerups:
                if powerup.active and ball.get_rect().colliderect(powerup.get_rect()):
                    powerup.active = False
                    if powerup.type == "multiball":
                        for _ in range(2):  # Add 2 extra balls
                            self.balls.append(Balls(ball.x, ball.y))
                            
    def update(self):
        if self.game_over or self.game_won:  # If game ended
            return  # Don't update anything
            
        # Move paddle based on key states
        self.paddle.move()
        
        
        for ball in self.balls:
            ball.move()
        self.collision_detection()
        
        ball = 0
        for balls in self.balls:
            if balls.active:
                ball += 1
        if ball == 0:  # If all balls are lost
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.balls.append(Balls())  # Add a new ball to start again
                global BALL_SPEED_X, BALL_SPEED_Y
                BALL_SPEED_X = 5
                BALL_SPEED_Y = 5
                
        if all(not brick.active for brick in self.bricks):  # If all bricks are destroyed
            self.level += 1
            # if self.level > 3:  # Win after 3 levels
            #     self.game_won = True
            # else:
            self.create_bricks()
            if self.level > 10 and not self.cheat_mode:
                    BALL_SPEED_X = BALL_SPEED_X + 0.5
                    BALL_SPEED_Y = BALL_SPEED_Y + 0.5
            for ball in self.balls:
                if not self.cheat_mode:
                    ball.active = False
            self.balls.append(Balls())  # Start next level with a new ball

    def draw(self):
        screen.fill(BLACK)
        
        # Awesome Background Grid
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
            
        self.paddle.draw() 
        for ball in self.balls:
            ball.draw()
        
        for brick in self.bricks:
            brick.draw()
        
        # Draw UI text
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        ball = 0
        for balls in self.balls:
            if balls.active:
                ball += 1
        ball_count_text = self.small_font.render(f"Balls: {ball}", True, WHITE)
        screen.blit(ball_count_text, (SCREEN_WIDTH - 120, 50))

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
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                    game.paddle.is_moving_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.paddle.is_moving_right = True
                if event.key == pygame.K_r and (game.game_over or game.game_won):
                    game = Game()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_c:
                    game.lives += 997
                    game.cheat_mode = not game.cheat_mode
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.paddle.is_moving_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
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