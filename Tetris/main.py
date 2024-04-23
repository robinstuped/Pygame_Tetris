# Import necessary modules
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 300, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Define constants
CELLSIZE = 20
ROWS = (HEIGHT - 120) // CELLSIZE
COLS = WIDTH // CELLSIZE
FPS = 24

# Define colors
BLACK = (21, 24, 29)
BLUE = (31, 25, 76)
RED = (252, 91, 122)
WHITE = (255, 255, 255)
GRID =  (31, 25, 132)

# Load images into dictionary
Assets = {
    1: pygame.image.load('Assets/1.png'),
    2: pygame.image.load('Assets/2.png'),
    3: pygame.image.load('Assets/3.png'),
    4: pygame.image.load('Assets/4.png')
}

# Load fonts
font = pygame.font.Font(None, 50)
font2 = pygame.font.SysFont('cursive', 25)

# Define Tetramino class
class TetrisShape:
    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1, 4)
        self.rotation = 0

    def image(self):
        """Return the current shape and its rotation"""
        return self.shape[self.rotation]

    def rotate(self):
        """Rotate the shape"""
        self.rotation = (self.rotation + 1) % len(self.shape)

# Define Tetris class
class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.board = [[0 for j in range(cols)] for i in range(rows)]
        self.next = None
        self.gameover = False
        self.new_figure()

    def draw_grid(self):
        """Draw the game grid"""
        for i in range(self.rows + 1):
            pygame.draw.line(win, GRID, (0, CELLSIZE * i), (WIDTH, CELLSIZE * i))
        for j in range(self.cols):
            pygame.draw.line(win, GRID, (CELLSIZE * j, 0), (CELLSIZE * j, HEIGHT - 120))

    def new_figure(self):
        """Generate a new tetromino figure"""
        if not self.next:
            self.next = TetrisShape(5, 0)
        self.figure = self.next
        self.next = TetrisShape(5, 0)
        
    def move_left(self):
        """Move the current figure left"""
        self.figure.x -= 1
        if self.intersects():
            self.figure.x += 1
            
    def freefall(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def move_right(self):
        """Move the current figure right"""
        self.figure.x += 1
        if self.intersects():
            self.figure.x -= 1

    def move_down(self):
        """Move the current figure down"""
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def rotate(self):
        """Rotate the current figure"""
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation

    def intersects(self):
        """Check if the current figure intersects with the grid"""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x
                    if (
                        block_row >= self.rows
                        or block_col >= self.cols
                        or block_col < 0
                        or self.board[block_row][block_col] > 0
                    ):
                        return True
        return False
    
    def remove_line(self):
        """Remove completed lines from the grid"""
        rerun = False

        for y in range(self.rows-1,0,-1):
            is_full = True
            
            for x in range(0, self.cols):
                if self.board[y][x] == 0:
                    is_full = False
                    
            if is_full:
                del self.board[y]
                self.board.insert(0,[0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
        # Recursive    
        if rerun:
            self.remove_line()

    def died(self):
        rect = pygame.Rect(100,100,(WIDTH - 100),(HEIGHT - 350))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)
        over = font.render("Game Over", True, WHITE)
        restart = font2.render("Press 'r' to restart!!!", True, RED)
        escape = font2.render("Press 'esc' to quit", True, RED)

        win.blit(over,(rect.centerx-over.get_width()//2, rect.y + 25))
        win.blit(restart,(rect.centerx-restart.get_width()//2, rect.y + 85))
        win.blit(escape,(rect.centerx-escape.get_width()//2, rect.y + 115))
            
    def freeze(self):
        """Freeze the current figure on the grid"""
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    self.board[i+self.figure.y][j+self.figure.x] = self.figure.color
                    
        self.remove_line()
        self.new_figure()
        if self.intersects():
            self.gameover = True

# Main function
def main():
    clock = pygame.time.Clock()
    counter = 0
    move_down = False
    can_move = True
    tetris = Tetris(ROWS, COLS)
	
    run = True
    while run:
        win.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT and tetris.gameover:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_left()
                elif event.key == pygame.K_RIGHT:
                    tetris.move_right()
                elif event.key == pygame.K_DOWN:
                    tetris.move_down()
                elif event.key == pygame.K_UP:
                    tetris.rotate()
                elif event.key == pygame.K_SPACE:
                    tetris.freefall()
                elif event.key == pygame.K_r:
                    tetris.__init__(ROWS, COLS)
                elif event.key == pygame.K_ESCAPE:
                    run = False
        

        # Update block position downwards at regular intervals
        counter += 1
        if counter >= 10000: 
            counter = 0

        if can_move:
            if counter % (FPS // (tetris.level * 2)) == 0 or move_down:
                if not tetris.gameover:
                    tetris.move_down()

        tetris.draw_grid()
        
        # Allows for the fallen img to stay on the screen
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.board[x][y] > 0:
                    val = tetris.board[x][y]
                    img = Assets[val]
                    win.blit(img, (y*CELLSIZE, x*CELLSIZE))
                    pygame.draw.rect(win, WHITE, (y*CELLSIZE, x*CELLSIZE,
                                        CELLSIZE, CELLSIZE), 1)
                    
        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in tetris.figure.image():
                        img = Assets[tetris.figure.color]
                        x = CELLSIZE * (tetris.figure.x + j)
                        y = CELLSIZE * (tetris.figure.y + i)
                        win.blit(img, (x, y))
                        pygame.draw.rect(win, WHITE, (x, y, CELLSIZE, CELLSIZE), 1)

        # Game Over Screen
        if tetris.gameover:
            tetris.died()

        # Generates the next image reveal
        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in tetris.next.image():
                        img = Assets[tetris.next.color]
                        x = CELLSIZE * (tetris.next.x + j - 4)
                        y = HEIGHT - 100 + CELLSIZE * (tetris.next.y + i)
        

        scoreimg = font.render(f'{tetris.score}', True, WHITE)
        levelimg = font2.render(f'Level : {tetris.level}', True, WHITE)
        win.blit(scoreimg, (250-scoreimg.get_width()//2, HEIGHT-110))
        win.blit(levelimg, (250-levelimg.get_width()//2, HEIGHT-30))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
